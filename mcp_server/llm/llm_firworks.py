import aiohttp
import json

class FireworksLLM:
    def __init__(self, api_key: str, model: str = "accounts/fireworks/models/kimi-k2-instruct-0905"):
        self.api_key = api_key
        self.model = model
        self.url = "https://api.fireworks.ai/inference/v1/chat/completions"

    async def generate(self, prompt: str) -> str:
        """Simple text completion, used when router says 'just answer like a normal LLM'."""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.url,
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ]
                }
            ) as resp:
                data = await resp.json()
                try:
                    return data["choices"][0]["message"]["content"]
                except:
                    return str(data)

    async def route_decision(self, system_prompt: str, user_prompt: str) -> dict:
        """Asks the LLM to return JSON tool-routing decision, prints full decision and reasoning."""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.url,
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json={
                    "model": self.model,
                    "response_format": {"type": "json_object"},
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ]
                }
            ) as resp:
                data = await resp.json()

                # Fireworks may return raw JSON directly
                if "choices" in data:
                    raw = data["choices"][0]["message"]["content"]
                else:
                    raw = data  # assume response is already JSON

                if isinstance(raw, str):
                    decision = json.loads(raw)
                else:
                    decision = raw

                # print full decision for debugging
                print("[AI decision JSON]:", json.dumps(decision, indent=2))

                # print reasoning if available
                reason = decision.get("reason")
                if reason:
                    print(f"[AI reasoning]: {reason}")

                return decision
