# mcp_server/tools/llm_tool.py
import asyncio
from typing import Any, Dict

class LLMClient:
    """Example async wrapper for your LLM API"""
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        self.api_key = api_key
        self.model = model
        # initialize your preferred LLM client here, e.g., OpenAI
        # self.client = OpenAI(api_key=api_key)

    async def generate(self, prompt: str, **kwargs) -> str:
        # example async call to LLM (replace with your actual client code)
        await asyncio.sleep(0.1)  # simulate network call
        return f"LLM response for prompt: {prompt}"


def register_llm_tool(server, llm_client: LLMClient):
    """Registers a single LLM tool on the MCP server"""

    async def llm_tool(prompt: str, options: Dict[str, Any] = None):
        """
        Args:
            prompt: the text prompt to send to LLM
            options: optional dictionary for extra LLM params (temperature, max_tokens, etc.)
        Returns:
            str: the LLM output
        """
        options = options or {}
        response = await llm_client.generate(prompt, **options)
        return response

    server.register_tool("llm", llm_tool)
