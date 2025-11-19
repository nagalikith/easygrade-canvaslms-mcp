from pydantic import BaseModel, Field
from typing import Optional


class CanvasConfig(BaseModel):
    token: str = Field(..., description="Canvas API token")
    domain: str = Field(..., description="Canvas domain, e.g. school.instructure.com")

    maxRetries: int = Field(3, description="Retry attempts for failed API calls")
    retryDelay: int = Field(1000, description="Delay between retries (ms)")
    timeout: int = Field(30000, description="Canvas API timeout (ms)")


class LoggingConfig(BaseModel):
    level: str = Field("info", description="Logging level")


class MCPServerConfig(BaseModel):
    name: str = Field("canvas-mcp-server", description="MCP server name")
    version: str = Field("1.0.0", description="Server version")

    canvas: CanvasConfig
    logging: LoggingConfig = LoggingConfig()

    @staticmethod
    def from_env():
        import os

        token = os.getenv("CANVAS_API_TOKEN")
        domain = os.getenv("CANVAS_DOMAIN")

        if not token or not domain:
            raise RuntimeError(
                "Missing required env vars: CANVAS_API_TOKEN and/or CANVAS_DOMAIN"
            )

        return MCPServerConfig(
            canvas=CanvasConfig(
                token=token,
                domain=domain,
                maxRetries=int(os.getenv("CANVAS_MAX_RETRIES", 3)),
                retryDelay=int(os.getenv("CANVAS_RETRY_DELAY", 1)),
                timeout=int(os.getenv("CANVAS_TIMEOUT", 30000)),
            ),
            logging=LoggingConfig(
                level=os.getenv("LOG_LEVEL", "info")
            ),
        )
