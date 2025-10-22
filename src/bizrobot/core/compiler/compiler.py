"""
Compiler: Plan -> deterministic DSL.
"""
from typing import Any, Dict, List
import uuid, datetime

class TaskCompiler:
    def __init__(self):
        self.version = "1.0"

    def compile_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        tasks: List[Dict[str, Any]] = []
        for step in plan.get("plan", []):
            task_id = uuid.uuid4().hex[:8]
            tasks.append({
                "task_id": task_id,
                "step_id": step.get("id"),
                "action": step.get("action", "unknown"),
                "target": step.get("target", "unknown"),
                "description": step.get("description", ""),
                "parameters": self._infer_parameters(step),
                "guards": self._default_guards(),
                "output": {"type": "json", "path": f"output/{task_id}.json"},
            })
        return {
            "dsl_version": self.version,
            "compiled_at": datetime.datetime.utcnow().isoformat(),
            "goal": plan.get("goal", ""),
            "tasks": tasks,
        }

    def _infer_parameters(self, step: Dict[str, Any]) -> Dict[str, Any]:
        act = step.get("action")
        if act == "call_api":
            return {"method": "POST", "headers": {}, "body": {}}
        if act == "web.fill_form":
            return {"selectors": {}, "values": {}}
        if act == "file.generate":
            return {"template": "default", "data": {}}
        return {}

    def _default_guards(self) -> Dict[str, Any]:
        return {
            "max_retries": 3,
            "timeout_seconds": 30,
            "preconditions": [],
            "postconditions": [],
            "dry_run": False,
        }
