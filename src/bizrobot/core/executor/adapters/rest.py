"""
REST adapter (mock). Replace with real httpx calls later.
"""
from typing import Dict, Any

class RESTAdapter:
    def run(self, step: Dict[str, Any]) -> Dict[str, Any]:
        # Simulate success. Wire real HTTP here (httpx) using step["parameters"].
        return {
            "ok": True,
            "capability": f"API::{step.get('target')}",
            "echo": step.get("parameters", {}),
        }
