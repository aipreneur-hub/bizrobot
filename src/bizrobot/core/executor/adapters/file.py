"""
File generator (mock).
"""
from typing import Dict, Any

class FileAdapter:
    def run(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "ok": True,
            "capability": "FILE::generate",
            "path": step.get("output", {}).get("path"),
        }
