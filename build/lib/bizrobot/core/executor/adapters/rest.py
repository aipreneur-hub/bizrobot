import httpx, asyncio
from .base import Adapter

class RestAdapter(Adapter):
    def __init__(self, http: httpx.AsyncClient, auth_provider): self.http=http; self.auth=auth_provider
    async def execute(self, step, ctx):
        cap = ctx["registry"].get(step["capability"])
        token = await self.auth.token(scope=cap["auth_scope"])
        # map inputs -> request (kept simple)
        resp = await self.http.post(cap["endpoint"], headers={"Authorization": f"Bearer {token}"}, json=step.get("inputs",{}), timeout=step.get("timeout_s",30))
        resp.raise_for_status()
        return resp.json()
