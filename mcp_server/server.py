import asyncio
import json
import traceback
from mcp.server.fastmcp import FastMCP, resource
from .client import CanvasClient
from .config import MCPServerConfig
from .tools import (
    register_course_tools,
    register_assignment_tools,
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
from .resources import register_resources


class CanvasMCPServer:
    def __init__(self, config: MCPServerConfig):
        self.config = config

        self.client = CanvasClient(
            token=config.canvas.token,
            domain=config.canvas.domain,
            scheme="http",
            max_retries=config.canvas.maxRetries,
            retry_delay=config.canvas.retryDelay,
            timeout=config.canvas.timeout,
        )

        self.server = FastMCP(
            name=config.name,
            version=config.version,
        )

        self._register_all_tools()
        self._register_resources()
        self._register_error_handlers()

    def _register_all_tools(self):
        register_course_tools(self.server, self.client)
        register_assignment_tools(self.server, self.client)
        register_module_tools(self.server, self.client)
        register_discussion_tools(self.server, self.client)
        register_announcement_tools(self.server, self.client)
        register_quiz_tools(self.server, self.client)
        register_file_tools(self.server, self.client)
        register_page_tools(self.server, self.client)
        register_calendar_tools(self.server, self.client)
        register_dashboard_tools(self.server, self.client)
        register_grade_tools(self.server, self.client)
        register_user_tools(self.server, self.client)
        register_account_tools(self.server, self.client)

    def _register_resources(self):
        register_resources(self.server, self.client)

    def _register_error_handlers(self):
        @self.server.error_handler
        async def errors(e):
            return {
                "error": str(e),
                "traceback": traceback.format_exc(),
            }

    async def run(self):
        await self.server.run(transport="stdio")
