from typing import Dict, Any
from .registry import DecisionRegistry
from .filters_engine import FILTERS
from ..utils.expression_parser import eval_condition

class DecisionEvaluator:
    def __init__(self, registry: DecisionRegistry | None = None):
        self.registry = registry or DecisionRegistry()

    def decide(self, project_id: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        tpl = self.registry.load(project_id)

        # 1) Filters
        filter_results = []
        for f in tpl.get("filters", []):
            passed, note = FILTERS[f](inputs)
            filter_results.append({"filter": f, "passed": passed, "note": note})
            if not passed:
                return {
                    "project_id": project_id,
                    "action": "escalate",
                    "confidence": 0.0,
                    "explanation": f"Filter failed: {f} -> {note}",
                    "filters": filter_results,
                }

        # 2) Decision logic (deterministic rules)
        decision = "escalate"
        for rule in tpl.get("decision_logic", []):
            cond = rule.get("if")
            then = rule.get("then")
            if cond is None:
                # fallback else branch
                decision = rule.get("else", decision)
                continue
            try:
                if eval_condition(cond, inputs):
                    decision = then
                    break
            except Exception as e:
                return {
                    "project_id": project_id,
                    "action": "escalate",
                    "confidence": 0.0,
                    "explanation": f"rule error: {e}",
                    "filters": filter_results,
                }

        # 3) Confidence simple heuristic
        confidence = 0.9 if decision != "escalate" else 0.5
        return {
            "project_id": project_id,
            "action": decision,
            "confidence": confidence,
            "explanation": "rule-based decision",
            "filters": filter_results,
        }
