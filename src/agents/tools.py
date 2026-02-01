import os
import sys
import json
from datetime import datetime
from dateutil import parser
from dotenv import load_dotenv
from langchain_core.tools import tool
from src.keywordsai_utils import KeywordsAIClient
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from supabase import create_client, Client

# Keywords AI tracing - task decorator for individual tools
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

# Load environment variables
load_dotenv()

# Initialize Keywords AI Client safely
try:
    kw_client = KeywordsAIClient()
except:
    kw_client = None

# Initialize Supabase
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
try:
    supabase: Client = create_client(supabase_url, supabase_key)
except Exception as e:
    print(f"Error initializing Supabase: {e}", file=sys.stderr)
    supabase = None


# Helper for creating server parameters
def get_server_params():
    return StdioServerParameters(
        command="docker",
        args=["run", "--rm", "-i", "--env-file", ".env", "canvas-lms-agent-mcp-canvas-lms"],
        env=None
    )


def get_thread_id_from_context():
    # Placeholder: In a real app, we'd pass this via context vars
    return None

async def run_mcp_tool(tool_name: str, arguments: dict = None) -> str:
    """
    Executes an MCP tool and returns the text content.
    Handles the connection, initialization, and result extraction.
    """
    arguments = arguments or {}
    try:
        async with stdio_client(get_server_params()) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(tool_name, arguments=arguments)
                
                # Extract text content from the result
                text_content = ""
                if hasattr(result, 'content') and isinstance(result.content, list):
                    for item in result.content:
                        if hasattr(item, 'text'):
                            text_content += item.text
                else:
                    text_content = str(result)
                
                # Log critical creation events to Keywords AI
                if kw_client and "create" in tool_name:
                    kw_client.log_custom_event(
                        event_name=f"tool_execution_{tool_name}",
                        metadata={"arguments": str(arguments), "success": True}
                    )
                    
                return text_content
    except Exception as e:
        if kw_client:
             kw_client.log_custom_event(
                event_name=f"tool_error_{tool_name}",
                metadata={"error": str(e)}
            )
        return f"Error executing {tool_name}: {str(e)}"


def format_with_link(response_text: str, success_msg: str = "Operation successful") -> str:
    """
    Parses the response JSON and appends the html_url if present.
    """
    try:
        data = json.loads(response_text)
        # Handle array responses (take first item if it's a creation/update usually returning one item)
        # But usually creation returns a single object.
        target = data[0] if isinstance(data, list) and len(data) > 0 else data
        
        if isinstance(target, dict) and "html_url" in target:
            return f"{success_msg}. Link: {target['html_url']}\n\nDetails: {response_text}"
            
        return response_text
    except:
        return response_text


def parse_date_to_iso(date_str: str) -> str:
    """
    Parses a date string (natural language or ISO) and returns a strict ISO 8601 string.
    """
    if not date_str:
        return None
        
    try:
        # Try parsing with dateutil (handles "next Friday", "2023-10-01", etc.)
        dt = parser.parse(date_str)
        
        # If no timezone is specified, assume UTC (or let Canvas handle it, but UTC is safer)
        # Canvas expects ISO 8601: YYYY-MM-DDTHH:MM:SSZ
        return dt.isoformat()
    except Exception as e:
        print(f"[WARNING] Date parsing failed for '{date_str}': {e}", file=sys.stderr)
        # Return original string if parsing fails, let Canvas API validate it
        return date_str


# --- CORE TOOLS ---

@tool
@task(name="canvas_health_check")
async def canvas_health_check():
    """Check the health and connectivity of the Canvas API."""
    return await run_mcp_tool("canvas_health_check")


# --- COURSE TOOLS ---

@tool
@task(name="get_canvas_courses")
async def get_canvas_courses():
    """Retrieves the list of Canvas courses."""
    return await run_mcp_tool("canvas_list_courses", {"include_ended": False})

@tool
@task(name="get_canvas_course")
async def get_canvas_course(course_id: str):
    """Get detailed information about a specific course."""
    return await run_mcp_tool("canvas_get_course", {"course_id": int(course_id)})

@tool
@task(name="create_canvas_course")
async def create_canvas_course(account_id: int, name: str, course_code: str = None, start_at: str = None, end_at: str = None, license: str = None, is_public: bool = False):
    """Create a new course in Canvas."""
    args = {"account_id": account_id, "name": name}
    if course_code: args["course_code"] = course_code
    if start_at: args["start_at"] = start_at
    if end_at: args["end_at"] = end_at
    if license: args["license"] = license
    if is_public: args["is_public"] = is_public
    
    response = await run_mcp_tool("canvas_create_course", args)
    return format_with_link(response, f"Course '{name}' created")

@tool
@task(name="update_canvas_course")
async def update_canvas_course(course_id: int, name: str = None, course_code: str = None):
    """Update an existing course in Canvas."""
    args = {"course_id": course_id}
    if name: args["name"] = name
    if course_code: args["course_code"] = course_code
    
    response = await run_mcp_tool("canvas_update_course", args)
    return format_with_link(response, "Course updated")


# --- ASSIGNMENT TOOLS ---

@tool
@task(name="get_course_assignments")
async def get_course_assignments(course_id: str):
    """Retrieves the list of assignments for a specific Canvas course."""
    return await run_mcp_tool("canvas_list_assignments", {"course_id": int(course_id)})

@tool
@task(name="get_canvas_assignment")
async def get_canvas_assignment(course_id: int, assignment_id: int):
    """Get detailed information about a specific assignment."""
    return await run_mcp_tool("canvas_get_assignment", {"course_id": course_id, "assignment_id": assignment_id})

@tool
@task(name="create_canvas_assignment")
async def create_canvas_assignment(course_id: str, assignment_name: str, due_date: str = None, points: int = 0, description: str = ""):
    """Creates a new ASSIGNMENT (graded work, homework) in a specific Canvas course. Do NOT use for announcements."""
    args = {
        "course_id": int(course_id),
        "name": assignment_name,
        "points_possible": points,
        "description": description
    }
    if due_date:
        args["due_at"] = parse_date_to_iso(due_date)
        
    response = await run_mcp_tool("canvas_create_assignment", args)
    return format_with_link(response, f"Assignment '{assignment_name}' created")

@tool
@task(name="update_canvas_assignment")
async def update_canvas_assignment(course_id: int, assignment_id: int, name: str = None, description: str = None, due_at: str = None, points_possible: int = None, published: bool = None):
    """Update an existing assignment."""
    args = {"course_id": course_id, "assignment_id": assignment_id}
    if name: args["name"] = name
    if description: args["description"] = description
    if due_at: args["due_at"] = parse_date_to_iso(due_at)
    if points_possible is not None: args["points_possible"] = points_possible
    if published is not None: args["published"] = published
    
    response = await run_mcp_tool("canvas_update_assignment", args)
    return format_with_link(response, "Assignment updated")

@tool
@task(name="list_assignment_groups")
async def list_assignment_groups(course_id: int):
    """List assignment groups for a course."""
    return await run_mcp_tool("canvas_list_assignment_groups", {"course_id": course_id})


# --- ANNOUNCEMENT TOOLS ---

@tool
@task(name="create_canvas_announcement")
async def create_canvas_announcement(course_id: str, title: str, message: str, delayed_post_at: str = None):
    """Creates a new ANNOUNCEMENT (message to students, news) in a specific Canvas course. Do NOT use for assignments."""
    args = {
        "course_id": int(course_id),
        "title": title,
        "message": message
    }
    if delayed_post_at:
        args["delayed_post_at"] = parse_date_to_iso(delayed_post_at)
        
    response = await run_mcp_tool("canvas_create_announcement", args)
    return format_with_link(response, f"Announcement '{title}' created")

@tool
@task(name="list_announcements")
async def list_announcements(course_id: int):
    """List all announcements in a course."""
    return await run_mcp_tool("canvas_list_announcements", {"course_id": course_id})


# --- SUBMISSION & GRADING TOOLS ---

@tool
@task(name="get_submissions")
async def get_submissions(course_id: str, assignment_id: str):
    """Retrieves submissions for a specific assignment (teacher view, gets all)."""
    # Note: Using get_submission with user_id='self' gets user's submission.
    # To get ALL submissions, we typically need a different endpoint or tool.
    # The MCP tool 'canvas_get_submission' takes user_id.
    # We'll map this to getting 'self' for now or handle the limitation.
    # However, for teachers, list_assignments with include_submission gives some info.
    return await run_mcp_tool("canvas_get_submission", {"course_id": int(course_id), "assignment_id": int(assignment_id), "user_id": "self"})

@tool
@task(name="get_canvas_submission")
async def get_canvas_submission(course_id: int, assignment_id: int, user_id: int = None):
    """Get submission details for an assignment."""
    args = {"course_id": course_id, "assignment_id": assignment_id}
    if user_id: args["user_id"] = user_id
    return await run_mcp_tool("canvas_get_submission", args)

@tool
@task(name="submit_canvas_assignment")
async def submit_canvas_assignment(course_id: int, assignment_id: int, submission_type: str, body: str = None, url: str = None):
    """Submit work for an assignment."""
    args = {"course_id": course_id, "assignment_id": assignment_id, "submission_type": submission_type}
    if body: args["body"] = body
    if url: args["url"] = url
    
    response = await run_mcp_tool("canvas_submit_assignment", args)
    return format_with_link(response, "Assignment submitted")

@tool
@task(name="submit_canvas_grade")
async def submit_canvas_grade(course_id: int, assignment_id: int, user_id: int, grade: str, comment: str = None):
    """Submit a grade for a student's assignment (teacher only)."""
    args = {"course_id": course_id, "assignment_id": assignment_id, "user_id": user_id, "grade": grade}
    if comment: args["comment"] = comment
    
    response = await run_mcp_tool("canvas_submit_grade", args)
    return format_with_link(response, "Grade submitted")


# --- DISCUSSION TOOLS ---

@tool
@task(name="list_discussion_topics")
async def list_discussion_topics(course_id: int):
    """List all discussion topics in a course."""
    return await run_mcp_tool("canvas_list_discussion_topics", {"course_id": course_id})

@tool
@task(name="get_discussion_topics")
async def get_discussion_topics(course_id: str):
    """Retrieves discussion topics (forums) for a specific Canvas course (Alias for list_discussion_topics)."""
    return await run_mcp_tool("canvas_list_discussion_topics", {"course_id": int(course_id)})

@tool
@task(name="get_discussion_topic")
async def get_discussion_topic(course_id: int, topic_id: int):
    """Get details of a specific discussion topic."""
    return await run_mcp_tool("canvas_get_discussion_topic", {"course_id": course_id, "topic_id": topic_id})

@tool
@task(name="get_full_discussion_entry")
async def get_full_discussion_entry(course_id: str, topic_id: str):
    """Retrieves full discussion entries for a specific topic."""
    return await run_mcp_tool("canvas_get_discussion_topic", {"course_id": int(course_id), "topic_id": int(topic_id)})

@tool
@task(name="post_to_discussion")
async def post_to_discussion(course_id: int, topic_id: int, message: str):
    """Post a message to a discussion topic."""
    response = await run_mcp_tool("canvas_post_to_discussion", {"course_id": course_id, "topic_id": topic_id, "message": message})
    return format_with_link(response, "Posted to discussion")


# --- QUIZ TOOLS ---

@tool
@task(name="list_quizzes")
async def list_quizzes(course_id: int):
    """List all quizzes in a course."""
    return await run_mcp_tool("canvas_list_quizzes", {"course_id": course_id})

@tool
@task(name="get_quiz")
async def get_quiz(course_id: int, quiz_id: int):
    """Get details of a specific quiz."""
    return await run_mcp_tool("canvas_get_quiz", {"course_id": course_id, "quiz_id": quiz_id})

@tool
@task(name="create_quiz")
async def create_quiz(course_id: int, title: str, description: str = None, quiz_type: str = "assignment", time_limit: int = None, published: bool = False, due_at: str = None):
    """Create a new quiz in a course."""
    args = {"course_id": course_id, "title": title, "quiz_type": quiz_type, "published": published}
    if description: args["description"] = description
    if time_limit: args["time_limit"] = time_limit
    if due_at: args["due_at"] = parse_date_to_iso(due_at)
    
    response = await run_mcp_tool("canvas_create_quiz", args)
    return format_with_link(response, f"Quiz '{title}' created")

@tool
@task(name="start_quiz_attempt")
async def start_quiz_attempt(course_id: int, quiz_id: int):
    """Start a new quiz attempt."""
    return await run_mcp_tool("canvas_start_quiz_attempt", {"course_id": course_id, "quiz_id": quiz_id})

@tool
@task(name="create_quiz_question")
async def create_quiz_question(course_id: int, quiz_id: int, question_name: str, question_text: str, question_type: str, points_possible: int = 1, answers: list = None):
    """
    Create a new question for a quiz.
    
    Args:
        course_id: ID of the course
        quiz_id: ID of the quiz
        question_name: Name of the question
        question_text: Text of the question (HTML supported)
        question_type: Type of question. Options: 'multiple_choice_question', 'true_false_question', 'short_answer_question', 'essay_question'
        points_possible: Points for the question
        answers: List of dictionaries with 'text', 'weight' (100 for correct, 0 for incorrect), and optional 'comments'.
                 Example: [{"text": "Answer A", "weight": 100}, {"text": "Answer B", "weight": 0}]
    """
    args = {
        "course_id": course_id,
        "quiz_id": quiz_id,
        "question_name": question_name,
        "question_text": question_text,
        "question_type": question_type,
        "points_possible": points_possible
    }
    if answers:
        args["answers"] = answers
        
    return await run_mcp_tool("canvas_create_quiz_question", args)


# --- MODULE TOOLS ---

@tool
@task(name="list_modules")
async def list_modules(course_id: int):
    """List all modules in a course."""
    return await run_mcp_tool("canvas_list_modules", {"course_id": course_id})

@tool
@task(name="get_module")
async def get_module(course_id: int, module_id: int):
    """Get details of a specific module."""
    return await run_mcp_tool("canvas_get_module", {"course_id": course_id, "module_id": module_id})

@tool
@task(name="list_module_items")
async def list_module_items(course_id: int, module_id: int):
    """List all items in a module."""
    return await run_mcp_tool("canvas_list_module_items", {"course_id": course_id, "module_id": module_id})

@tool
@task(name="get_module_item")
async def get_module_item(course_id: int, module_id: int, item_id: int):
    """Get details of a specific module item."""
    return await run_mcp_tool("canvas_get_module_item", {"course_id": course_id, "module_id": module_id, "item_id": item_id})

@tool
@task(name="mark_module_item_complete")
async def mark_module_item_complete(course_id: int, module_id: int, item_id: int):
    """Mark a module item as complete."""
    return await run_mcp_tool("canvas_mark_module_item_complete", {"course_id": course_id, "module_id": module_id, "item_id": item_id})


# --- FILE TOOLS ---

@tool
@task(name="list_canvas_files")
async def list_canvas_files(course_id: int, folder_id: int = None):
    """List files in a course or folder."""
    args = {"course_id": course_id}
    if folder_id: args["folder_id"] = folder_id
    return await run_mcp_tool("canvas_list_files", args)

@tool
@task(name="get_canvas_file")
async def get_canvas_file(file_id: int):
    """Get information about a specific file."""
    return await run_mcp_tool("canvas_get_file", {"file_id": file_id})

@tool
@task(name="list_canvas_folders")
async def list_canvas_folders(course_id: int):
    """List folders in a course."""
    return await run_mcp_tool("canvas_list_folders", {"course_id": course_id})


# --- PAGE TOOLS ---

@tool
@task(name="list_canvas_pages")
async def list_canvas_pages(course_id: int):
    """List pages in a course."""
    return await run_mcp_tool("canvas_list_pages", {"course_id": course_id})

@tool
@task(name="get_canvas_page")
async def get_canvas_page(course_id: int, page_url: str):
    """Get content of a specific page."""
    return await run_mcp_tool("canvas_get_page", {"course_id": course_id, "page_url": page_url})


# --- USER & ACCOUNT TOOLS ---

@tool
@task(name="get_user_profile")
async def get_user_profile():
    """Get current user's profile."""
    return await run_mcp_tool("canvas_get_user_profile")

@tool
@task(name="update_user_profile")
async def update_user_profile(name: str = None, bio: str = None):
    """Update current user's profile."""
    args = {}
    if name: args["name"] = name
    if bio: args["bio"] = bio
    return await run_mcp_tool("canvas_update_user_profile", args)

@tool
@task(name="enroll_user")
async def enroll_user(course_id: int, user_id: int, role: str = "StudentEnrollment"):
    """Enroll a user in a course."""
    return await run_mcp_tool("canvas_enroll_user", {"course_id": course_id, "user_id": user_id, "role": role})

@tool
@task(name="get_course_grades")
async def get_course_grades(course_id: int):
    """Get grades for a course."""
    return await run_mcp_tool("canvas_get_course_grades", {"course_id": course_id})

@tool
@task(name="get_user_grades")
async def get_user_grades():
    """Get all grades for the current user."""
    return await run_mcp_tool("canvas_get_user_grades")

@tool
@task(name="get_account")
async def get_account(account_id: int):
    """Get account details."""
    return await run_mcp_tool("canvas_get_account", {"account_id": account_id})

@tool
@task(name="list_account_courses")
async def list_account_courses(account_id: int):
    """List courses for an account."""
    return await run_mcp_tool("canvas_list_account_courses", {"account_id": account_id})

@tool
@task(name="list_account_users")
async def list_account_users(account_id: int):
    """List users for an account."""
    return await run_mcp_tool("canvas_list_account_users", {"account_id": account_id})

@tool
@task(name="create_user")
async def create_user(account_id: int, name: str, unique_id: str, password: str = None):
    """Create a new user in an account."""
    args = {
        "account_id": account_id,
        "user": {"name": name},
        "pseudonym": {"unique_id": unique_id}
    }
    if password:
        args["pseudonym"]["password"] = password
    
    response = await run_mcp_tool("canvas_create_user", args)
    return format_with_link(response, f"User '{name}' created")


# --- MISC TOOLS ---

@tool
@task(name="list_calendar_events")
async def list_calendar_events(start_date: str = None, end_date: str = None):
    """List calendar events."""
    args = {}
    if start_date: args["start_date"] = start_date
    if end_date: args["end_date"] = end_date
    return await run_mcp_tool("canvas_list_calendar_events", args)

@tool
@task(name="get_upcoming_assignments")
async def get_upcoming_assignments(limit: int = 10):
    """Get upcoming assignment due dates."""
    return await run_mcp_tool("canvas_get_upcoming_assignments", {"limit": limit})

@tool
@task(name="get_canvas_dashboard")
async def get_canvas_dashboard():
    """Get user's dashboard information."""
    return await run_mcp_tool("canvas_get_dashboard")

@tool
@task(name="get_canvas_dashboard_cards")
async def get_canvas_dashboard_cards():
    """Get dashboard course cards."""
    return await run_mcp_tool("canvas_get_dashboard_cards")

@tool
@task(name="list_rubrics")
async def list_rubrics(course_id: int):
    """List rubrics for a course."""
    return await run_mcp_tool("canvas_list_rubrics", {"course_id": course_id})

@tool
@task(name="get_rubric")
async def get_rubric(course_id: int, rubric_id: int):
    """Get details of a specific rubric."""
    return await run_mcp_tool("canvas_get_rubric", {"course_id": course_id, "rubric_id": rubric_id})

@tool
@task(name="create_canvas_rubric")
async def create_canvas_rubric(course_id: str, title: str, description: str):
    """Creates a new rubric in a specific Canvas course (Note: Functionality may be limited in MCP)."""
    # This was present in old tools.py but not clearly in index.ts. 
    # We will attempt to use a generic 'canvas_create_rubric' if it existed, but index.ts doesn't show it.
    # Leaving as placeholder or returning error to be safe.
    return "Error: Rubric creation is not currently supported by the backend."

@tool
@task(name="list_conversations")
async def list_conversations():
    """List user's conversations."""
    return await run_mcp_tool("canvas_list_conversations")

@tool
@task(name="get_conversation")
async def get_conversation(conversation_id: int):
    """Get details of a specific conversation."""
    return await run_mcp_tool("canvas_get_conversation", {"conversation_id": conversation_id})

@tool
@task(name="send_canvas_message")
async def send_canvas_message(user_id: str, subject: str, body: str):
    """Sends a message to a Canvas user using the create_conversation tool."""
    response = await run_mcp_tool("canvas_create_conversation", {
        "recipients": [user_id],
        "subject": subject,
        "body": body
    })
    return format_with_link(response, "Message sent")

@tool
@task(name="list_notifications")
async def list_notifications():
    """List user's notifications."""
    return await run_mcp_tool("canvas_list_notifications")

@tool
@task(name="get_syllabus")
async def get_syllabus(course_id: int):
    """Get course syllabus."""
    return await run_mcp_tool("canvas_get_syllabus", {"course_id": course_id})


# --- LOCAL TOOLS ---

@tool
@task(name="save_template")
def save_template(name: str, content: str):
    """Saves a template to the Supabase database."""
    if not supabase:
        return "Error: Supabase client not initialized."
    try:
        response = supabase.table("templates").insert({"name": name, "content": content}).execute()
        return "Template saved."
    except Exception as e:
        return f"Error saving template: {str(e)}"

@tool
@task(name="load_template")
def load_template(name: str):
    """Loads a template from the Supabase database."""
    if not supabase:
        return "Error: Supabase client not initialized."
    try:
        response = supabase.table("templates").select("content").eq("name", name).execute()
        if response.data:
            return response.data[0]['content']
        return "Template not found."
    except Exception as e:
        return f"Error loading template: {str(e)}"

@tool
@task(name="read_local_file")
def read_local_file(path: str):
    """Reads a local file (syllabus, markdown, text) from the filesystem."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return f"Error: File not found at {path}"
    except Exception as e:
        return f"Error reading file: {str(e)}"


# Export all tools as a list
all_tools = [
    # Core
    canvas_health_check,
    
    # Course
    get_canvas_courses,
    get_canvas_course,
    create_canvas_course,
    update_canvas_course,
    get_course_grades,
    get_syllabus,
    
    # Assignment
    get_course_assignments,
    get_canvas_assignment,
    create_canvas_assignment,
    update_canvas_assignment,
    list_assignment_groups,
    get_upcoming_assignments,
    
    # Submission & Grading
    get_submissions,
    get_canvas_submission,
    submit_canvas_assignment,
    submit_canvas_grade,
    
    # Announcement
    create_canvas_announcement,
    list_announcements,
    
    # Discussion
    list_discussion_topics,
    get_discussion_topics,
    get_discussion_topic,
    get_full_discussion_entry,
    post_to_discussion,
    
    # Module
    list_modules,
    get_module,
    list_module_items,
    get_module_item,
    mark_module_item_complete,
    
    # Quiz
    list_quizzes,
    get_quiz,
    create_quiz,
    start_quiz_attempt,
    create_quiz_question,
    
    # File
    list_canvas_files,
    get_canvas_file,
    list_canvas_folders,
    
    # Page
    list_canvas_pages,
    get_canvas_page,
    
    # User & Account
    get_user_profile,
    update_user_profile,
    enroll_user,
    get_user_grades,
    get_account,
    list_account_courses,
    list_account_users,
    create_user,
    
    # Misc
    list_calendar_events,
    get_canvas_dashboard,
    get_canvas_dashboard_cards,
    list_rubrics,
    get_rubric,
    create_canvas_rubric,
    list_conversations,
    get_conversation,
    send_canvas_message,
    list_notifications,
    
    # Local
    save_template,
    load_template,
    read_local_file
]
