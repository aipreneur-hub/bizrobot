from typing import Dict, Any
from ..decision_engine.evaluator import DecisionEvaluator
from ..decision_engine.registry import DecisionRegistry
from ..decision_engine.roi_evaluator import compute_roi

_registry = DecisionRegistry()
_evaluator = DecisionEvaluator(_registry)

def make_decision(project_id: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
    result = _evaluator.decide(project_id, inputs)
    tpl = _registry.load(project_id)
    action_value = result.get("action") or result.get("decision") or "none"
    result["roi_score"] = compute_roi(tpl, action_value)
    return result
