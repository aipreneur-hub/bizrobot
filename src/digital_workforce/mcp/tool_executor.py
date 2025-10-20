from typing import Dict, Any
from .registry import TOOLS

def call_tool(tool_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
    if tool_id not in TOOLS:
        return {"status": "error", "message": f"unknown tool {tool_id}"}
    # Mock side-effect
    return {"status": "ok", "reference_id": f"MOCK-{tool_id}-001", "echo": params}
