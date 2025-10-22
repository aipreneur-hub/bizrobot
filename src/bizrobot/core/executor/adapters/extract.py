"""
ExtractAdapter: mock data extraction capability.
"""
from typing import Dict, Any

class ExtractAdapter:
    def run(self, step: Dict[str, Any]) -> Dict[str, Any]:
        target = step.get("target", "unknown")
        return {
            "ok": True,
            "capability": f"EXTRACT::{target}",
            "data": {"sample_key": "sample_value"},
        }
