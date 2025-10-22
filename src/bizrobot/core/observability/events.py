"""
Simple event logger to stdout (can be replaced with structured sink).
"""
from typing import Dict, Any
import json, time, sys

class EventBus:
    def emit(self, event_type: str, data: Dict[str, Any]):
        payload = {"type": event_type, "ts": time.time(), "data": data}
        sys.stdout.write("[EVENT] " + json.dumps(payload) + "\n")
        sys.stdout.flush()
