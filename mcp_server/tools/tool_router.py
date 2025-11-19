import inspect
import json
import re


class ToolRouter:
    def __init__(self, server, canvas_tools, llm):
        self.server = server
        self.canvas_tools = canvas_tools
        self.llm = llm

        self.tool_aliases = {
            "create_course": "canvas_create_course",
            "list_courses": "canvas_list_courses",
            "get_course": "canvas_get_course",
            "update_course": "canvas_update_course",
        }

    # ----------------------------
    # NORMALIZATION HELPERS
    # ----------------------------

    def normalize_key(self, key: str):
        """camelCase → snake_case, strip weird chars, lowercase everything."""
        if not isinstance(key, str):
            return key

        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", key)
        s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)
        snake = s2.replace("-", "_").replace(" ", "_").lower()

        return snake

    def smart_normalize_args(self, tool_fn, args: dict):
        """Automatically match LLM arguments to real tool signature."""
        sig = inspect.signature(tool_fn)
        params = sig.parameters
        valid_params = list(params.keys())
        accepts_kwargs = any(
            p.kind == inspect.Parameter.VAR_KEYWORD for p in params.values()
        )

        normalized = {}

        for raw_key, value in args.items():
            key = self.normalize_key(raw_key)

            # exact match
            if key in valid_params:
                normalized[key] = value
                continue

            # fuzzy match
            fuzzy_hits = [p for p in valid_params if key in p or p in key]
            if fuzzy_hits:
                normalized[fuzzy_hits[0]] = value
                continue

            # fallback to **kwargs
            if accepts_kwargs:
                normalized[key] = value
                continue

        return normalized

    # ----------------------------
    # MAIN ROUTER
    # ----------------------------

    async def route(self, query: str):
        q = query.lower()

        # instant keyword matches
        if "courses" in q and ("list" in q or "show" in q):
            return await self.server.call_tool("canvas_list_courses", {})
        if "assignments" in q:
            return await self.server.call_tool("canvas_list_assignments", {})
        if "modules" in q:
            return await self.server.call_tool("canvas_list_modules", {})
        if "grades" in q:
            return await self.server.call_tool("canvas_get_user_grades", {})

        # ask LLM what to do
        system_prompt = """
        You are CanvasBot, an AI agent controlling a Canvas LMS.
        Respond only with JSON:
        {
          "action": "tool" or "llm",
          "tool_name": "something",
          "arguments": {},
          "reason": ""
        }
        """

        decision = await self.llm.route_decision(system_prompt, query)

        if not isinstance(decision, dict):
            return await self.llm.generate(query)

        action = decision.get("action")
        tool_name = decision.get("tool_name")
        args = decision.get("arguments", {})

        # map tool alias to real MCP tool
        if tool_name in self.tool_aliases:
            tool_name = self.tool_aliases[tool_name]

        if action == "llm" or tool_name not in self.canvas_tools:
            return await self.llm.generate(query)

        # SMART NORMALIZATION HERE
        tool_fn = self.canvas_tools[tool_name]
        args = self.smart_normalize_args(tool_fn, args)

        # EXECUTE TOOL
        return await self.server.call_tool(tool_name, args)
