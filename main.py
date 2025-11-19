import asyncio
import os
from mcp.server.fastmcp import FastMCP
from mcp_server.config import MCPServerConfig
from mcp_server.client import CanvasClient
from mcp_server.llm.llm_firworks import FireworksLLM
from mcp_server.tools import (
    register_course_tools,
    register_assignment_tools,
    register_assignment_group_tools,
    register_submission_tools,
    register_module_tools,
    register_discussion_tools,
    register_announcement_tools,
    register_quiz_tools,
    register_file_tools,
    register_page_tools,
    register_calendar_tools,
    register_dashboard_tools,
    register_grade_tools,
    register_user_tools,
    register_account_tools,
)
from mcp_server.resources import attach_resource_handlers
from mcp_server.tools.tool_router import ToolRouter


async def main():
    # load config
    config = MCPServerConfig.from_env()

    # init Canvas client
    client = CanvasClient(
        token=config.canvas.token,
        domain=config.canvas.domain,
        max_retries=config.canvas.maxRetries,
        retry_delay=config.canvas.retryDelay,
        timeout=config.canvas.timeout,
    )

    # init MCP server
    server = FastMCP(name=config.name)

    # attach resources and tools
    attach_resource_handlers(server, client)
    register_course_tools(server, client)
    register_assignment_tools(server, client)
    register_assignment_group_tools(server, client)
    register_submission_tools(server, client)
    register_module_tools(server, client)
    register_discussion_tools(server, client)
    register_announcement_tools(server, client)
    register_quiz_tools(server, client)
    register_file_tools(server, client)
    register_page_tools(server, client)
    register_calendar_tools(server, client)
    register_dashboard_tools(server, client)
    register_grade_tools(server, client)
    register_user_tools(server, client)
    register_account_tools(server, client)

    # init LLM
    llm_client = FireworksLLM(api_key=os.getenv("FIREWORKS_API_KEY"))

    # setup tool router
    canvas_tools = {name: server._tool_manager.get_tool(name) for name in server._tool_manager._tools}
    router = ToolRouter(server, canvas_tools, llm_client)

    @server.tool()
    async def ask_router_tool(query: str):
        return await router.route(query)

    print("MCP AI agent ready! Type commands in English (Ctrl+C to quit).")

    # CLI loop
    while True:
        try:
            query = input("> ")
            result = await ask_router_tool(query)
            print(result)
        except KeyboardInterrupt:
            print("\nShutting down MCP server...")
            break
        except Exception as e:
            print(f"[Error]: {e}")


if __name__ == "__main__":
    asyncio.run(main())
