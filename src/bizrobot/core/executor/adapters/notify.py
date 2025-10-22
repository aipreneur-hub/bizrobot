"""
NotifyAdapter: mock notification capability.
"""
from typing import Dict, Any

class NotifyAdapter:
    def run(self, step: Dict[str, Any]) -> Dict[str, Any]:
        target = step.get("target", "unknown")
        return {
            "ok": True,
            "capability": f"NOTIFY::{target}",
            "status": "sent",
            "message": step.get("description", ""),
        }
