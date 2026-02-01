import asyncio
import os
import sys
import json
from typing import TypedDict, Literal
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent
print("DEBUG: after langgraph imports", file=sys.stderr)

# Keywords AI tracing - task decorator for individual agent nodes
try:
    from keywordsai_tracing.decorators import task
    TRACING_ENABLED = True
except ImportError:
    TRACING_ENABLED = False
    # Mock task decorator if tracing not available
    def task(name=None):  # noqa: ARG001
        def decorator(func):
            return func
        return decorator

# Import checkpointers (will try multiple options)
try:
    from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False

try:
    from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
    SQLITE_AVAILABLE = True
except ImportError:
    SQLITE_AVAILABLE = False

# Import all_tools from the tools module
from src.agents.tools import all_tools
from src.keywordsai_utils import KeywordsAIClient, determine_model_complexity
from src.agents.prompt_templates import CANVAS_EXECUTOR_PROMPT, SUPERVISOR_PROMPT, CONTENT_SPECIALIST_PROMPT

# Initialize Keywords AI Client
try:
    kw_client = KeywordsAIClient()
except:
    kw_client = None

# Load environment variables
load_dotenv()


# Define the AgentState
class AgentState(TypedDict):
    """State for the multi-agent system."""
    messages: list
    next: str


# Thread-local storage for request context (customer_id, thread_id)
_request_context = {}


def set_request_context(customer_identifier: str = None, thread_identifier: str = None, metadata: dict = None):
    """Set the request context for Keywords AI tracking."""
    global _request_context
    _request_context = {
        "customer_identifier": customer_identifier,
        "thread_identifier": thread_identifier,
        "metadata": metadata or {}
    }


def get_request_context() -> dict:
    """Get the current request context."""
    return _request_context


# Initialize Keywords AI LLM
def create_llm(agent_name: str = "default", model_name: str = "gpt-4o-mini"):
    """Create and return the Keywords AI LLM instance with tracing.

    Args:
        agent_name: Name of the agent for tracing purposes (supervisor, executor, specialist)
        model_name: Name of the model to use
    """
    # Get current request context for metadata
    ctx = get_request_context()

    # Build headers with Keywords AI specific parameters
    # These are passed via headers for LangChain compatibility
    headers = {
        'X-Keywords-Source': 'CanvasAI-MultiAgent',
        'X-Keywords-Cache-TTL': '3600',  # Semantic cache for 1 hour
        'X-Keywords-Agent': agent_name  # Track which agent is making the call
    }

    # Add customer/thread identifiers to headers if available
    if ctx.get("customer_identifier"):
        headers['X-Keywords-Customer-Id'] = ctx["customer_identifier"]
    if ctx.get("thread_identifier"):
        headers['X-Keywords-Thread-Id'] = ctx["thread_identifier"]

    return ChatOpenAI(
        base_url=os.getenv('KEYWORDSAI_BASE_URL', 'https://api.keywordsai.co/api/'),
        api_key=os.getenv('KEYWORDSAI_API_KEY'),
        model=model_name,
        temperature=0,
        default_headers=headers
    )

# Pre-initialize both models to avoid overhead
fast_llm = create_llm(model_name="gpt-4o-mini")
smart_llm = create_llm(model_name="gpt-4o")


# Node 1: Canvas_Executor - ReAct agent with all tools
def create_canvas_executor(llm):
    """Create the Canvas Executor agent with all tools."""
    
    # Use centralized prompt from templates
    system_prompt = CANVAS_EXECUTOR_PROMPT

    # Create ReAct agent with specific system prompt
    # Note: Using 'prompt' parameter for system instructions
    # OPTIMIZATION: Removed 'all_tools' to prevent full tool schema injection for simple queries.
    # We should only inject relevant tools, but for now, let's keep it simple.
    return create_react_agent(llm, all_tools, prompt=system_prompt)


@task(name="Canvas_Executor")
async def canvas_executor_node(state: AgentState) -> AgentState:
    """Canvas Executor node - handles Canvas operations."""
    print("[EXECUTOR] Starting Canvas_Executor", file=sys.stderr)

    # Dynamic Model Selection
    last_human = next((m for m in reversed(state["messages"]) if isinstance(m, HumanMessage)), None)
    input_text = last_human.content if last_human else ""
    
    model_choice = determine_model_complexity(input_text)
    
    # Use smart_llm for complex tasks, otherwise fast_llm
    # But we need to ensure the agent name is correct for tracing
    # Since fast_llm/smart_llm are pre-initialized with "default" or "gpt-4o-mini",
    # we might want to create a new instance with the correct agent name OR just use them.
    # For tracing to be perfect, we should ideally create a new one, but for performance, reuse.
    # Let's create a new one to keep tracing correct (overhead is minimal compared to LLM call).
    
    selected_llm = create_llm(agent_name="Canvas_Executor", model_name=model_choice)
    print(f"[EXECUTOR] Using model: {model_choice} for input: '{input_text[:30]}...'", file=sys.stderr)

    executor = create_canvas_executor(selected_llm)

    # Run the executor agent
    # OPTIMIZATION: Only pass the last 5 messages to reduce context window and latency
    # This prevents the agent from re-reading the entire conversation history every time
    recent_messages = state["messages"][-5:] if len(state["messages"]) > 5 else state["messages"]
    
    result = await executor.ainvoke({"messages": recent_messages})
    print(f"[EXECUTOR] Completed, returning {len(result['messages'])} messages", file=sys.stderr)

    # Debug: Log the last message from executor
    if result.get("messages"):
        last_msg = result["messages"][-1]
        msg_type = type(last_msg).__name__
        msg_content = getattr(last_msg, 'content', 'N/A')
        if isinstance(msg_content, str):
            preview = msg_content[:150] + "..." if len(msg_content) > 150 else msg_content
            print(f"[EXECUTOR] Last message type: {msg_type}, content preview: {preview}", file=sys.stderr)

    return {
        "messages": result["messages"],
        "next": "supervisor"
    }


# Node 2: Content_Specialist - Pure LLM node without tools
@task(name="Content_Specialist")
async def content_specialist_node(state: AgentState) -> AgentState:
    """Content Specialist node - drafts assignments and rubrics."""
    print("[SPECIALIST] Starting Content_Specialist", file=sys.stderr)

    # Dynamic Model Selection
    last_human = next((m for m in reversed(state["messages"]) if isinstance(m, HumanMessage)), None)
    input_text = last_human.content if last_human else ""
    
    model_choice = determine_model_complexity(input_text)
    
    # Content Specialist benefits most from smart model
    llm = create_llm(agent_name="Content_Specialist", model_name=model_choice)
    print(f"[SPECIALIST] Using model: {model_choice}", file=sys.stderr)

    # Add system prompt for the content specialist
    system_prompt = SystemMessage(
        content=CONTENT_SPECIALIST_PROMPT
    )

    # Combine system prompt with existing messages
    # OPTIMIZATION: Only use last 5 messages + system prompt
    recent_messages = state["messages"][-5:] if len(state["messages"]) > 5 else state["messages"]
    messages = [system_prompt] + recent_messages

    # Get response from LLM
    response = await llm.ainvoke(messages)
    print(f"[SPECIALIST] Completed, response length: {len(response.content)}", file=sys.stderr)

    # QUALITY CHECK & LOGGING
    if kw_client:
        score = 1.0 if len(response.content) > 50 else 0.5
        if "error" in response.content.lower():
            score = 0.0
            
        kw_client.log_with_score(
            input_messages=[{"role": "user", "content": "Draft content"}], # Simplified for log
            output_message={"role": "assistant", "content": response.content},
            score=score,
            score_name="content_quality",
            metadata={"agent": "Content_Specialist"}
        )

    return {
        "messages": state["messages"] + [response],
        "next": "supervisor"
    }


# Node 3: Supervisor - Router that decides next action
@task(name="Supervisor")
async def supervisor_node(state: AgentState) -> AgentState:
    """Supervisor node - routes to appropriate worker or finishes."""
    print(f"[SUPERVISOR] Processing {len(state['messages'])} messages", file=sys.stderr)
    
    # Supervisor is a router, usually fast model is enough
    # But if routing logic is complex, we might want smart model
    # For now, stick to default (which is usually mini) unless we want to make it dynamic too.
    # Let's keep it fast for responsiveness.
    llm = create_llm(agent_name="Supervisor", model_name="gpt-4o-mini")

    # System prompt for the supervisor
    system_prompt = SystemMessage(
        content=SUPERVISOR_PROMPT
    )

    # Combine system prompt with existing messages
    # OPTIMIZATION: Only use last 5 messages + system prompt
    recent_messages = state["messages"][-5:] if len(state["messages"]) > 5 else state["messages"]
    messages = [system_prompt] + recent_messages

    # Get routing decision from supervisor
    response = await llm.ainvoke(messages)

    # Parse the JSON response
    try:
        decision = json.loads(response.content)
        next_step = decision.get("next", "FINISH")
        print(f"[SUPERVISOR] Parsed JSON decision: {next_step}", file=sys.stderr)
    except json.JSONDecodeError:
        # If JSON parsing fails, try to extract the decision from the text
        print(f"[SUPERVISOR] JSON parse failed, using fallback. Response: {response.content[:200]}", file=sys.stderr)
        content = response.content.lower()
        if "canvas_executor" in content:
            next_step = "Canvas_Executor"
        elif "content_specialist" in content:
            next_step = "Content_Specialist"
        else:
            next_step = "FINISH"
        print(f"[SUPERVISOR] Fallback decision: {next_step}", file=sys.stderr)

    print(f"[SUPERVISOR] Routing to: {next_step}", file=sys.stderr)

    return {
        "messages": state["messages"] + [response],
        "next": next_step
    }


# Router function to determine the next node
def route_after_supervisor(state: AgentState) -> Literal["Canvas_Executor", "Content_Specialist", "FINISH"]:
    """Route to the next node based on supervisor's decision."""
    next_step = state.get("next", "FINISH")

    if next_step == "Canvas_Executor":
        return "Canvas_Executor"
    elif next_step == "Content_Specialist":
        return "Content_Specialist"
    elif next_step == "FINISH":
        return "FINISH"
    else:
        return "FINISH"


def route_back_to_supervisor(state: AgentState) -> Literal["supervisor"]:
    """Route workers back to supervisor."""
    return "supervisor"


# Create the graph
def create_agent_app():
    print("DEBUG: create_agent_app start", file=sys.stderr)
    """Create and return the multi-agent supervisor graph."""
    # Create the state graph
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("Canvas_Executor", canvas_executor_node)
    workflow.add_node("Content_Specialist", content_specialist_node)


    # Add edges from supervisor to workers (conditional)
    workflow.add_conditional_edges(
        "supervisor",
        route_after_supervisor,
        {
            "Canvas_Executor": "Canvas_Executor",
            "Content_Specialist": "Content_Specialist",
            "FINISH": END
        }
    )

    # Add edges from workers back to supervisor
    workflow.add_edge("Canvas_Executor", "supervisor")
    workflow.add_edge("Content_Specialist", "supervisor")

    # Set entry point
    workflow.set_entry_point("supervisor")

    # Setup persistent checkpointer
    checkpointer = None
    database_url = os.getenv('SUPABASE_DATABASE_URL')

    # NOTE: Async checkpointers (AsyncPostgresSaver, AsyncSqliteSaver) cannot be initialized
    # at module import time because there's no running event loop.
    # For now, we'll use MemorySaver. TODO: Implement lazy async checkpointer initialization.

    # Try PostgreSQL first (if URL is provided and package is available)
    if False and database_url and POSTGRES_AVAILABLE:
        try:
            print("[INFO] Attempting PostgreSQL connection to Supabase...", file=sys.stderr)
            print("[INFO] Disabling prepared statements for PgBouncer compatibility", file=sys.stderr)

            # Import async connection pool for async server compatibility
            from psycopg_pool import AsyncConnectionPool
            from psycopg.rows import dict_row

            # Create async connection pool with prepare_threshold=None and open=False
            # This is REQUIRED for Supabase Transaction Pooler (port 6543) to avoid DuplicatePreparedStatement errors
            # open=False prevents auto-opening which requires an event loop
            pool = AsyncConnectionPool(
                conninfo=database_url,
                kwargs={
                    "prepare_threshold": None,  # Disable prepared statements for PgBouncer
                    "autocommit": True,
                    "row_factory": dict_row
                },
                min_size=1,
                max_size=10,
                open=False  # Don't auto-open at creation time
            )

            # Create async checkpointer with the pool
            # The pool will open automatically when first used in an async context
            checkpointer = AsyncPostgresSaver(pool)

            # Note: checkpointer.setup() will be called automatically by LangGraph when needed

            print("[SUCCESS] Supabase Persistence Active (PostgreSQL)", file=sys.stderr)
            print(f"[INFO] Connected to: {database_url.split('@')[1] if '@' in database_url else 'database'}", file=sys.stderr)
            print("[INFO] Using async connection pool with prepared statements disabled", file=sys.stderr)
        except Exception as e:
            print("[ERROR] PostgreSQL Connection Failed", file=sys.stderr)
            print(f"[ERROR] Error Type: {type(e).__name__}", file=sys.stderr)
            print(f"[ERROR] Details: {str(e)}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            checkpointer = None

    # Try SQLite as fallback (local file persistence)
    if False and checkpointer is None and SQLITE_AVAILABLE:
        try:
            print("[INFO] Using SQLite for local persistence...", file=sys.stderr)
            sqlite_path = os.path.join(os.path.dirname(__file__), "checkpoints.db")

            # Use AsyncSqliteSaver for async compatibility
            checkpointer = AsyncSqliteSaver.from_conn_string(sqlite_path)

            print("[SUCCESS] SQLite Persistence Active", file=sys.stderr)
            print(f"[INFO] Checkpoint database: {sqlite_path}", file=sys.stderr)
        except Exception as e:
            print(f"[ERROR] SQLite Setup Failed: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            checkpointer = None

    # Final fallback to in-memory (no persistence)
    if checkpointer is None:
        print("[WARNING] No persistent storage available", file=sys.stderr)
        if database_url and not POSTGRES_AVAILABLE:
            print("[INFO] Install: pip install langgraph-checkpoint-postgres psycopg psycopg-binary", file=sys.stderr)
        elif not SQLITE_AVAILABLE:
            print("[INFO] Install: pip install langgraph-checkpoint-sqlite", file=sys.stderr)
        print("[INFO] Using in-memory checkpointing (conversations will not persist)", file=sys.stderr)
        from langgraph.checkpoint.memory import MemorySaver
        checkpointer = MemorySaver()

    # Compile the graph
    return workflow.compile(checkpointer=checkpointer)


# Global app instance for import
try:
    app = create_agent_app()
except Exception as e:
    print(f"Error creating agent app: {e}", file=sys.stderr)
    app = None


async def main():
    """Main function to run the agent interactively."""
    if not app:
        print("Agent app failed to initialize.")
        return

    print("Multi-Agent Canvas LMS System ready! Type 'quit' or 'exit' to stop.")

    # Configuration for the thread
    config = {"configurable": {"thread_id": "1"}}

    while True:
        try:
            # Get user input
            user_input = input("\nUser: ")

            if user_input.lower() in ['quit', 'exit']:
                print("Goodbye!")
                break

            print("Processing...")

            # Create initial state with user message
            initial_state = {
                "messages": [HumanMessage(content=user_input)],
                "next": ""
            }

            # Run the agent
            final_state = await app.ainvoke(initial_state, config=config)

            # Get the last AI message
            if final_state.get("messages"):
                for msg in reversed(final_state["messages"]):
                    if isinstance(msg, AIMessage):
                        # Skip supervisor routing messages (JSON)
                        try:
                            json.loads(msg.content)
                            continue
                        except (json.JSONDecodeError, AttributeError):
                            print(f"\nAgent: {msg.content}\n")
                            break

        except KeyboardInterrupt:
            print("\nInterrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == '__main__':
    # Use ProactorEventLoop on Windows for subprocesses
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    asyncio.run(main())
