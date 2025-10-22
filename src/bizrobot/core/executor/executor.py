"""
Executor: runs DSL tasks with basic retries + event logging.
"""
from typing import Dict, Any, List
import time
from bizrobot.core.executor.adapters import RESTAdapter, BrowserAdapter, FileAdapter
from bizrobot.core.observability.events import EventBus
from bizrobot.core.executor.adapters import (
    RESTAdapter,
    BrowserAdapter,
    FileAdapter,
)
from bizrobot.core.executor.adapters.extract import ExtractAdapter
from bizrobot.core.executor.adapters.notify import NotifyAdapter


class Executor:
    def __init__(self, events: EventBus | None = None):
        self.events = events or EventBus()
        self.adapters = {
            "call_api": RESTAdapter(),
            "web.fill_form": BrowserAdapter(),
            "file.generate": FileAdapter(),
        }

        self.adapters = {
            "call_api": RESTAdapter(),
            "web.fill_form": BrowserAdapter(),
            "file.generate": FileAdapter(),
            "extract_data": ExtractAdapter(),
            "notify": NotifyAdapter(),
        }
        
    def execute(self, dsl: Dict[str, Any]) -> Dict[str, Any]:
        results: Dict[str, Any] = {}
        tasks: List[Dict[str, Any]] = dsl.get("tasks", [])

        for step in tasks:
            action = step.get("action")
            adapter = self.adapters.get(action)
            if adapter is None:
                raise RuntimeError(f"No adapter for action: {action}")

            guards = step.get("guards", {})
            retries = int(guards.get("max_retries", 0))
            timeout = int(guards.get("timeout_seconds", 30))

            self.events.emit("StepStarted", {"step_id": step["step_id"], "action": action})

            attempt = 0
            last_err: str | None = None
            while attempt <= retries:
                try:
                    # naive timeout simulation (real: use httpx/playwright timeouts)
                    start = time.time()
                    out = adapter.run(step)
                    if time.time() - start > timeout:
                        raise TimeoutError("Step timeout exceeded")

                    if not out.get("ok"):
                        raise RuntimeError("Adapter returned non-ok")

                    results[step["task_id"]] = out
                    self.events.emit("StepSucceeded", {"step_id": step["step_id"], "task_id": step["task_id"]})
                    break
                except Exception as e:
                    last_err = str(e)
                    self.events.emit("StepFailed", {"step_id": step["step_id"], "task_id": step["task_id"], "error": last_err})
                    attempt += 1

            if last_err and step["task_id"] not in results:
                raise RuntimeError(f"Step {step['step_id']} failed after retries: {last_err}")

        self.events.emit("RunCompleted", {"tasks": len(tasks)})
        return results

