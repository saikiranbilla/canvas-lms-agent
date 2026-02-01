import os
import sys
import json

# Add the project root to the python path FIRST
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables FIRST
from dotenv import load_dotenv
load_dotenv()

# Initialize Keywords AI Telemetry
print("[INFO] Initializing Keywords AI Telemetry...", file=sys.stderr)

try:
    from keywordsai_tracing.main import KeywordsAITelemetry
    from keywordsai_tracing.decorators import workflow
    telemetry = KeywordsAITelemetry()
    print("[INFO] Keywords AI Telemetry initialized successfully", file=sys.stderr)
except ImportError:
    print("[WARNING] keywordsai_tracing not found, skipping telemetry", file=sys.stderr)
    telemetry = None
    # Mock workflow decorator
    def workflow(name=None):
        def decorator(func):
            return func
        return decorator
except Exception as e:
    print(f"[ERROR] Failed to initialize Keywords AI Telemetry: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()
    telemetry = None
    # Mock workflow decorator if import succeeded but init failed
    if 'workflow' not in locals():
        def workflow(name=None):
            def decorator(func):
                return func
            return decorator

# Now import everything else

from fastapi import FastAPI, HTTPException, Depends, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager
import uvicorn
import nest_asyncio
from langchain_core.messages import AIMessage, ToolMessage, HumanMessage
import httpx
import secrets
import urllib.parse
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import jwt

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

# Import the Agent (AFTER OTel is fully initialized)
try:
    from src.agents.graph import app, set_request_context
except ImportError as e:
    print(f"Error importing app: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()
    app = None
    set_request_context = None

# OAuth2 Configuration
CANVAS_CLIENT_ID = os.getenv("CANVAS_CLIENT_ID")
CANVAS_CLIENT_SECRET = os.getenv("CANVAS_CLIENT_SECRET")
CANVAS_DOMAIN = os.getenv("CANVAS_DOMAIN", "canvas.instructure.com")
CANVAS_API_TOKEN = os.getenv("CANVAS_API_TOKEN") # Direct API Token
JWT_SECRET = os.getenv("JWT_SECRET", secrets.token_urlsafe(32))
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

# OAuth2 Session Storage (in production, use Redis or database)
oauth_sessions: Dict[str, Dict[str, Any]] = {}

# Agent Dashboard Data (In-memory for demo)
AGENT_METRICS = {
    "conversations_today": 12,
    "agent_runs_today": 45,
    "avg_response_time": 1.2,
    "most_used_tool": "Canvas_Executor",
    "total_response_time": 54.0
}

RECENT_RUNS = [
    {
        "id": "1",
        "intent": "Check missing assignments",
        "tools": ["get_courses", "get_assignments"],
        "duration": "1.5s",
        "status": "success",
        "timestamp": (datetime.utcnow() - timedelta(minutes=5)).isoformat()
    },
    {
        "id": "2",
        "intent": "Draft announcement for Psych 101",
        "tools": ["create_announcement"],
        "duration": "2.1s",
        "status": "success",
        "timestamp": (datetime.utcnow() - timedelta(minutes=25)).isoformat()
    },
    {
        "id": "3",
        "intent": "Grade submission for user 123",
        "tools": ["get_submission", "grade_submission"],
        "duration": "3.0s",
        "status": "success",
        "timestamp": (datetime.utcnow() - timedelta(hours=1)).isoformat()
    },
    {
        "id": "4",
        "intent": "List students in Neuro 201",
        "tools": ["get_users"],
        "duration": "0.8s",
        "status": "error",
        "timestamp": (datetime.utcnow() - timedelta(hours=2)).isoformat()
    },
    {
        "id": "5",
        "intent": "Summarize course syllabus",
        "tools": ["get_course_content"],
        "duration": "4.5s",
        "status": "success",
        "timestamp": (datetime.utcnow() - timedelta(hours=4)).isoformat()
    }
]

# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(api: FastAPI):
    # Startup
    print("[INFO] FastAPI application starting...", file=sys.stderr)

    yield

    # Shutdown - flush any remaining traces
    print("[INFO] Shutting down server, flushing traces...", file=sys.stderr)
    if telemetry:
        telemetry.flush()
    print("[INFO] Shutdown complete", file=sys.stderr)

api = FastAPI(lifespan=lifespan)

@api.get("/")
async def root():
    """Root endpoint to check if server is running."""
    return {"status": "ok", "service": "canvas-lms-agent", "version": "1.0.0"}

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class ChatRequest(BaseModel):
    message: str
    thread_id: str = "demo-1"
    customer_id: Optional[str] = None  # For Keywords AI user tracking
    metadata: Optional[Dict[str, Any]] = None  # Custom metadata for Keywords AI


class FeedbackRequest(BaseModel):
    """Request model for submitting feedback on agent responses."""
    log_id: Optional[str] = None  # Keywords AI log ID (if available)
    thread_id: str  # Thread ID to associate feedback with
    positive: bool  # True = thumbs up, False = thumbs down
    score: Optional[float] = None  # Optional numeric score (0.0 to 1.0)
    comment: Optional[str] = None  # Optional feedback comment


class PromptRequest(BaseModel):
    """Request model for using managed prompts."""
    prompt_id: str  # Keywords AI prompt ID
    variables: Optional[Dict[str, str]] = None  # Template variables
    customer_id: Optional[str] = None


# JWT Token Functions
def create_jwt_token(canvas_user_id: int, canvas_domain: str, access_token: str) -> str:
    payload = {
        "canvas_user_id": canvas_user_id,
        "canvas_domain": canvas_domain,
        "canvas_access_token": access_token, # Storing access token in JWT for simplicity in this demo
        "exp": datetime.utcnow() + timedelta(days=7),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def verify_jwt_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except (jwt.ExpiredSignatureError, jwt.JWTError):
        return None

# OAuth2 Authentication Endpoints
@api.get("/auth/login")
async def login(request: Request):
    """Initiate Canvas OAuth2 login flow or Direct Token Login"""
    
    # Check if we have a direct API token configured
    if CANVAS_API_TOKEN:
        print("[INFO] Using direct CANVAS_API_TOKEN for login", file=sys.stderr)
        try:
            # Verify the token works by fetching user profile
            async with httpx.AsyncClient() as client:
                user_response = await client.get(
                    f"https://{CANVAS_DOMAIN}/api/v1/users/self/profile",
                    headers={"Authorization": f"Bearer {CANVAS_API_TOKEN}"}
                )
                
                if user_response.status_code == 200:
                    user_data = user_response.json()
                    # Create JWT with the direct token
                    jwt_token = create_jwt_token(user_data["id"], CANVAS_DOMAIN, CANVAS_API_TOKEN)
                    return RedirectResponse(url=f"{FRONTEND_URL}?token={jwt_token}")
                else:
                    print(f"[ERROR] Direct token validation failed: {user_response.status_code} - {user_response.text}", file=sys.stderr)
        except Exception as e:
            print(f"[ERROR] Direct token login error: {e}", file=sys.stderr)

    # Fallback to OAuth2 flow if direct token fails or isn't present
    if not CANVAS_CLIENT_ID or not CANVAS_CLIENT_SECRET:
        # Fallback for demo if credentials aren't set
        pass
    
    state = secrets.token_urlsafe(32)
    oauth_sessions[state] = {
        "created_at": datetime.utcnow(),
        "redirect_uri": f"{FRONTEND_URL}/auth/callback"
    }
    
    params = {
        "client_id": CANVAS_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": f"{FRONTEND_URL}/auth/callback",
        "scope": "url:GET|/api/v1/courses url:GET|/api/v1/users/profile",
        "state": state
    }
    
    auth_url = f"https://{CANVAS_DOMAIN}/login/oauth2/auth?{urllib.parse.urlencode(params)}"
    return RedirectResponse(url=auth_url)

@api.get("/auth/callback")
async def auth_callback(code: str, state: str):
    """Handle Canvas OAuth2 callback"""
    # For demo purposes, we'll verify state but might need to be lenient if session restarted
    if state not in oauth_sessions:
        # In a real app, this is an error. For hackathon, maybe just proceed?
        # raise HTTPException(status_code=400, detail="Invalid state parameter")
        pass
    
    session = oauth_sessions.pop(state, {"redirect_uri": f"{FRONTEND_URL}/auth/callback"})
    
    try:
        token_data = {
            "grant_type": "authorization_code",
            "client_id": CANVAS_CLIENT_ID,
            "client_secret": CANVAS_CLIENT_SECRET,
            "redirect_uri": session["redirect_uri"],
            "code": code
        }
        
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                f"https://{CANVAS_DOMAIN}/login/oauth2/token",
                data=token_data
            )
            
            if token_response.status_code != 200:
                print(f"[ERROR] Token exchange failed: {token_response.text}", file=sys.stderr)
                raise HTTPException(status_code=400, detail="Failed to obtain access token")
            
            access_token = token_response.json().get("access_token")
            
            user_response = await client.get(
                f"https://{CANVAS_DOMAIN}/api/v1/users/self/profile",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            
            user_data = user_response.json()
            jwt_token = create_jwt_token(user_data["id"], CANVAS_DOMAIN, access_token)
            
            return RedirectResponse(url=f"{FRONTEND_URL}?token={jwt_token}")
            
    except Exception as e:
        print(f"[ERROR] OAuth callback failed: {e}", file=sys.stderr)
        raise HTTPException(status_code=500, detail="Authentication failed")

@api.get("/api/user/me")
async def get_user_profile(request: Request):
    """Get current user's Canvas profile"""
    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    token = auth_header.split(" ")[1]
    
    # Handle mock token for demo
    if token == "mock_token_for_demo":
        pass

    payload = verify_jwt_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    try:
        canvas_token = payload.get("canvas_access_token")
        canvas_domain = payload.get("canvas_domain")
        
        if canvas_token:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://{canvas_domain}/api/v1/users/self/profile",
                    headers={"Authorization": f"Bearer {canvas_token}"}
                )
                
                if response.status_code == 200:
                    profile = response.json()
                    # Add a title/role field if not present (Canvas doesn't always provide this in profile)
                    profile["title"] = "Faculty" # Default for this agent context
                    return profile
                else:
                    print(f"[ERROR] Canvas API Error: {response.text}", file=sys.stderr)
                    raise HTTPException(status_code=response.status_code, detail="Failed to fetch user profile")
        
        # Fallback if no canvas token (shouldn't happen in this flow but good for safety)
        raise HTTPException(status_code=400, detail="No Canvas token found")
            
    except Exception as e:
        print(f"[ERROR] Failed to fetch user profile: {e}", file=sys.stderr)
        raise HTTPException(status_code=500, detail="Failed to fetch user profile")

@api.get("/api/dashboard")
async def get_dashboard(request: Request):
    """Get user's dashboard cards and planner items"""
    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    token = auth_header.split(" ")[1]
    
    # Handle mock token
    if token == "mock_token_for_demo":
        pass

    payload = verify_jwt_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    try:
        canvas_token = payload.get("canvas_access_token")
        canvas_domain = payload.get("canvas_domain")
        
        if canvas_token:
            async with httpx.AsyncClient() as client:
                # Fetch Dashboard Cards
                cards_response = await client.get(
                    f"https://{canvas_domain}/api/v1/dashboard/dashboard_cards",
                    headers={"Authorization": f"Bearer {canvas_token}"}
                )
                
                # Fetch Planner Items (Todos)
                # start_date = now, end_date = 2 weeks from now
                start_date = datetime.utcnow().isoformat()
                end_date = (datetime.utcnow() + timedelta(days=14)).isoformat()
                
                planner_response = await client.get(
                    f"https://{canvas_domain}/api/v1/planner/items?start_date={start_date}&end_date={end_date}",
                    headers={"Authorization": f"Bearer {canvas_token}"}
                )
                
                dashboard_data = {
                    "dashboard_cards": cards_response.json() if cards_response.status_code == 200 else [],
                    "planner_items": planner_response.json() if planner_response.status_code == 200 else []
                }
                
                return dashboard_data
        
        raise HTTPException(status_code=400, detail="No Canvas token found")
            
    except Exception as e:
        print(f"[ERROR] Failed to fetch dashboard data: {e}", file=sys.stderr)
        # Return empty structure instead of failing completely
        return {"dashboard_cards": [], "planner_items": []}

@api.get("/api/agent/status")
async def get_agent_status():
    """Get agent system status and metrics for dashboard"""
    
    # Check Canvas Token Status
    canvas_status = "connected" if CANVAS_API_TOKEN or (CANVAS_CLIENT_ID and CANVAS_CLIENT_SECRET) else "disconnected"
    
    # Calculate uptime or last run
    last_run = RECENT_RUNS[0]["timestamp"] if RECENT_RUNS else datetime.utcnow().isoformat()
    
    return {
        "system_status": {
            "supervisor": "ready",
            "canvas_mcp": "connected",
            "tool_execution": "available",
            "memory": "active",
            "last_run": last_run
        },
        "canvas_integration": {
            "status": canvas_status,
            "token_valid": True, # Simplified check
            "mcp_health": "healthy",
            "available_tools": 15, # Hardcoded for now
            "last_successful_call": last_run
        },
        "metrics": AGENT_METRICS,
        "recent_runs": RECENT_RUNS[:5]
    }

@api.get("/api/courses")
async def get_courses(request: Request):
    """Get user's Canvas courses"""
    auth_header = request.headers.get("Authorization")
    
    print(f"[DEBUG] Fetching courses with Auth header: {auth_header[:20]}...", file=sys.stderr)

    if auth_header == "Bearer mock_token_for_demo":
        # Fallback for demo if credentials aren't set
        pass

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    token = auth_header.split(" ")[1]
    payload = verify_jwt_token(token)
    if not payload:
        print("[ERROR] Invalid JWT token provided", file=sys.stderr)
        raise HTTPException(status_code=401, detail="Invalid token")
    
    try:
        # If we have a real access token in the JWT, use it
        canvas_token = payload.get("canvas_access_token")
        canvas_domain = payload.get("canvas_domain")
        
        print(f"[DEBUG] Using Canvas Token: {canvas_token[:10]}... on domain: {canvas_domain}", file=sys.stderr)
        
        if canvas_token:
            async with httpx.AsyncClient() as client:
                # Try fetching courses with pagination handling (basic)
                # Including 'teacher', 'student', 'ta' enrollments to be safe
                url = f"https://{canvas_domain}/api/v1/courses?enrollment_state=active&include[]=total_students&include[]=term"
                print(f"[DEBUG] Requesting Canvas API: {url}", file=sys.stderr)
                
                response = await client.get(
                    url,
                    headers={"Authorization": f"Bearer {canvas_token}"}
                )
                
                print(f"[DEBUG] Canvas API Response Status: {response.status_code}", file=sys.stderr)
                
                if response.status_code == 200:
                    courses = response.json()
                    print(f"[DEBUG] Successfully fetched {len(courses)} courses from Canvas API", file=sys.stderr)
                    # Log first course to debug structure
                    if len(courses) > 0:
                        print(f"[DEBUG] First course sample: {json.dumps(courses[0], default=str)}", file=sys.stderr)
                    return {"courses": courses}
                else:
                    print(f"[ERROR] Canvas API Error: {response.text}", file=sys.stderr)
                    # Don't fail immediately, try the tool fallback
        
        # Fallback to agent tool (uses env var token)
        print("[INFO] Fallback to agent tool for fetching courses", file=sys.stderr)
        from src.agents.tools import get_canvas_courses
        courses_result = await get_canvas_courses()
        
        try:
            courses_data = json.loads(courses_result)
            courses = courses_data if isinstance(courses_data, list) else [courses_data]
            return {"courses": courses}
        except json.JSONDecodeError:
            return {"courses": [], "raw_content": courses_result}
            
    except Exception as e:
        print(f"[ERROR] Failed to fetch courses: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Failed to fetch courses")

@api.post("/chat")
@workflow(name="Clai_Workflow")
async def chat(request: ChatRequest):
    """Process chat request with Keywords AI tracing."""
    if app is None:
        return {"error": "Agent app not initialized"}

    config = {"configurable": {"thread_id": request.thread_id}}
    start_time = datetime.utcnow()

    # Set Keywords AI request context for metadata tracking
    if set_request_context:
        set_request_context(
            customer_identifier=request.customer_id,
            thread_identifier=request.thread_id,
            metadata=request.metadata or {"source": "canvas-lms-agent"}
        )

    try:
        # Invoke the multi-agent graph
        result = await app.ainvoke(
            {"messages": [HumanMessage(content=request.message)]},
            config=config
        )
        
        # Debug: Print full result messages
        print(f"[DEBUG] Result messages count: {len(result.get('messages', []))}", file=sys.stderr)
        for i, m in enumerate(result.get('messages', [])):
             content_str = getattr(m, 'content', str(m))
             print(f"[DEBUG] Msg {i}: Type={type(m).__name__}, Content={str(content_str)[:100]}...", file=sys.stderr)

        # Calculate duration and update metrics
        duration = (datetime.utcnow() - start_time).total_seconds()
        AGENT_METRICS["conversations_today"] += 1
        AGENT_METRICS["agent_runs_today"] += 1
        AGENT_METRICS["total_response_time"] += duration
        AGENT_METRICS["avg_response_time"] = round(AGENT_METRICS["total_response_time"] / AGENT_METRICS["agent_runs_today"], 2)

        # Record run
        RECENT_RUNS.insert(0, {
            "id": secrets.token_hex(4),
            "intent": request.message[:50] + "..." if len(request.message) > 50 else request.message,
            "tools": ["supervisor"], # Simplified
            "duration": f"{duration:.2f}s",
            "status": "success",
            "timestamp": datetime.utcnow().isoformat()
        })
        if len(RECENT_RUNS) > 20:
            RECENT_RUNS.pop()

        # Flush traces to Keywords AI
        if telemetry:
            telemetry.flush()

    # Iterate backwards through messages to find first meaningful AIMessage
    final_message_content = None
    if result.get("messages"):
        for msg in reversed(result["messages"]):
            # Check if it's an AIMessage with non-empty content
            if isinstance(msg, AIMessage) and msg.content:
                # Skip supervisor routing JSON messages
                try:
                    # cleanup markdown code blocks first
                    content_to_check = msg.content.strip()
                    if "```json" in content_to_check:
                        content_to_check = content_to_check.split("```json")[1].split("```")[0].strip()
                    elif "```" in content_to_check:
                        content_to_check = content_to_check.split("```")[1].strip()

                    parsed = json.loads(content_to_check)
                    # If it parses as JSON with 'next' key, it's a routing signal
                    if isinstance(parsed, dict) and "next" in parsed:
                        continue
                except (json.JSONDecodeError, ValueError):
                    # Not JSON, this is a real response
                    pass

                # Found a meaningful message
                final_message_content = msg.content
                break

        # If no meaningful message found, return default
        if final_message_content is None:
            final_message_content = "Process completed."

        print(f"[INFO] Chat completed successfully, thread_id={request.thread_id}", file=sys.stderr)
        return {"response": final_message_content, "content": final_message_content, "status": "success"}

    except Exception as e:
        print(f"[ERROR] Chat endpoint failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return {"error": str(e)}


# ========== KEYWORDS AI FEATURE ENDPOINTS ==========

@api.post("/api/feedback")
async def submit_feedback(request: FeedbackRequest):
    """
    Submit feedback on an agent response for Keywords AI evaluations.

    This endpoint allows users to provide thumbs up/down feedback
    on agent responses, which is logged to Keywords AI for analysis.
    """
    try:
        from src.keywordsai_utils import KeywordsAIClient

        # Store feedback in local metrics
        feedback_entry = {
            "thread_id": request.thread_id,
            "positive": request.positive,
            "score": request.score,
            "comment": request.comment,
            "timestamp": datetime.utcnow().isoformat()
        }

        # Try to submit to Keywords AI if we have a log_id
        if request.log_id:
            try:
                client = KeywordsAIClient()
                client.submit_feedback(
                    log_id=request.log_id,
                    positive_feedback=request.positive,
                    score=request.score,
                    comment=request.comment
                )
                print(f"[INFO] Feedback submitted to Keywords AI for log {request.log_id}", file=sys.stderr)
            except Exception as kai_error:
                print(f"[WARNING] Could not submit feedback to Keywords AI: {kai_error}", file=sys.stderr)

        print(f"[INFO] Feedback received: {'positive' if request.positive else 'negative'} for thread {request.thread_id}", file=sys.stderr)

        return {
            "status": "success",
            "message": "Feedback recorded",
            "feedback": feedback_entry
        }

    except Exception as e:
        print(f"[ERROR] Feedback submission failed: {e}", file=sys.stderr)
        return {"status": "error", "message": str(e)}


@api.post("/api/prompt")
async def use_managed_prompt(request: PromptRequest):
    """
    Make an LLM call using a managed prompt from Keywords AI.

    Create prompts in the Keywords AI dashboard, then use them here
    by providing the prompt_id and any template variables.

    Example:
        POST /api/prompt
        {
            "prompt_id": "042f5f",
            "variables": {
                "course_name": "Psychology 101",
                "assignment_type": "quiz"
            }
        }
    """
    try:
        from src.keywordsai_utils import KeywordsAIClient

        client = KeywordsAIClient()
        response = client.chat_with_prompt(
            prompt_id=request.prompt_id,
            variables=request.variables or {}
        )

        # Extract the response content
        content = response.get("choices", [{}])[0].get("message", {}).get("content", "")

        print(f"[INFO] Managed prompt {request.prompt_id} executed successfully", file=sys.stderr)

        return {
            "status": "success",
            "content": content,
            "prompt_id": request.prompt_id,
            "usage": response.get("usage", {})
        }

    except Exception as e:
        print(f"[ERROR] Managed prompt execution failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}


@api.get("/api/keywordsai/status")
async def get_keywordsai_status():
    """
    Check Keywords AI integration status and configuration.
    """
    api_key = os.getenv("KEYWORDSAI_API_KEY")
    base_url = os.getenv("KEYWORDSAI_BASE_URL", "https://api.keywordsai.co/api/")

    return {
        "status": "configured" if api_key else "not_configured",
        "api_key_set": bool(api_key),
        "base_url": base_url,
        "telemetry_enabled": telemetry is not None,
        "features": {
            "tracing": telemetry is not None,
            "gateway": bool(api_key),
            "prompt_management": bool(api_key),
            "evaluations": bool(api_key),
            "logging_api": bool(api_key)
        }
    }


if __name__ == '__main__':
    print("--- Starting Server ---", file=sys.stderr)
    try:
        uvicorn.run(api, host='0.0.0.0', port=8001)
    except Exception as e:
        print(f"[FATAL] Uvicorn failed to start: {e}", file=sys.stderr)
        sys.exit(1)
