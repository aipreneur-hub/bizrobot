from typing import Dict, Any
from ..models.cognitive_state import CognitiveState
from ..interfaces.decision_interface import make_decision
from ..interfaces.tool_interface import execute_action
from ..audit.audit_log import write_audit
from ..audit.roi_tracker import track_roi


def _resolve_final_decision(value):
    """Recursively resolve nested decision structures to a final string."""
    if isinstance(value, dict):
        if "decision" in value:
            return _resolve_final_decision(value["decision"])
        if "then" in value:
            return _resolve_final_decision(value["then"])
        if "else" in value:
            return _resolve_final_decision(value["else"])
        return None
    return value


def run_cycle(inputs: Dict[str, Any]) -> CognitiveState:
    """
    Generic U–T–D–A–L loop (Understand–Think–Decide–Act–Learn)
    Domain projects pass their decision context as `inputs`.
    """
    state = CognitiveState(inputs=inputs)
    decision = make_decision(project_id=inputs["project_id"], inputs=inputs)
    state.decision = decision

    write_audit("decision_made", decision)
    project_id = decision.get("project_id") or decision.get("context", {}).get("project_id", "unknown_project")
    track_roi(project_id, decision.get("roi_score", 0.0))

    # ✅ Flatten nested decision logic safely
    action_value = decision.get("action") or decision.get("decision")
    final_action = _resolve_final_decision(action_value)

    if not isinstance(final_action, str):
        print(f"⚠️  Cannot resolve valid action; skipping execution. Raw value: {final_action}")
        return state

    if final_action.startswith("skills."):
        outcome = execute_action(final_action, inputs)
    else:
        print(f"🧾 Final decision: {final_action} (no tool execution required)")
        outcome = {"status": "ok", "decision": final_action}

    state.outcome = outcome

    write_audit("action_executed", outcome)
    write_audit("learn", {"status": "ok"})
    return state
