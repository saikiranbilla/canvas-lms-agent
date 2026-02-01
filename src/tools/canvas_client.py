import asyncio
import json
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_canvas_agent():
    print("Starting Canvas Agent...", file=sys.stderr)
    server_params = StdioServerParameters(
        command="docker",
        args=["run", "--rm", "-i", "--env-file", ".env", "canvas-lms-agent-mcp-canvas-lms"],
        env=None 
    )

    print(f"Connecting to server: {server_params.command} {server_params.args}", file=sys.stderr)
    
    try:
        async with stdio_client(server_params) as (read, write):
            print("Connected to stdio.", file=sys.stderr)
            async with ClientSession(read, write) as session:
                # Initialize the connection
                print("Initializing session...", file=sys.stderr)
                await session.initialize()
                print("Session initialized.", file=sys.stderr)

                # List available tools
                print("Fetching available tools...", file=sys.stderr)
                tools = await session.list_tools()
                print("Available Tools:")
                for tool in tools.tools:
                    print(f"- {tool.name}")
                
                # Call canvas_list_courses tool
                print("\nCalling canvas_list_courses tool...", file=sys.stderr)
                try:
                    # The tool is named 'canvas_list_courses', not 'list_courses'
                    result = await session.call_tool("canvas_list_courses", arguments={})
                    print("Result from canvas_list_courses:")
                    
                    # Helper to serialize the result content
                    def serialize_content(content):
                        if isinstance(content, list):
                            return [serialize_content(item) for item in content]
                        if hasattr(content, 'text'):
                             return {"type": content.type, "text": content.text}
                        return str(content)

                    print(json.dumps(serialize_content(result.content), indent=2))
                except Exception as e:
                    print(f"Error calling canvas_list_courses: {e}", file=sys.stderr)

    except Exception as e:
        print(f"Error in stdio_client: {e}", file=sys.stderr)

if __name__ == "__main__":
    # Use ProactorEventLoop on Windows for subprocesses
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    try:
        asyncio.run(run_canvas_agent())
    except KeyboardInterrupt:
        print("Interrupted", file=sys.stderr)
