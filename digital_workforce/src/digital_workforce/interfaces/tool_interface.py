from typing import Dict, Any
from ..mcp.tool_executor import call_tool

def execute_action(action: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generic tool executor for decisions.
    External projects define mappings between decision actions and MCP tools.
    """
    return call_tool(action, inputs)
