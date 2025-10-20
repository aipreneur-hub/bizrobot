from typing import Dict, Any
from ..models.cognitive_state import CognitiveState
from ..interfaces.decision_interface import make_decision
from ..interfaces.tool_interface import execute_action
from ..audit.audit_log import write_audit
from ..audit.roi_tracker import track_roi

def run_cycle(inputs: Dict[str, Any]) -> CognitiveState:
    """
    Generic U–T–D–A–L loop (Understand–Think–Decide–Act–Learn)
    Domain projects pass their decision context as `inputs`.
    """
    state = CognitiveState(inputs=inputs)
    decision = make_decision(project_id=inputs["project_id"], inputs=inputs)
    state.decision = decision

    write_audit("decision_made", decision)
    track_roi(decision["project_id"], decision.get("roi_score", 0.0))

    outcome = execute_action(decision["action"], inputs)
    state.outcome = outcome

    write_audit("action_executed", outcome)
    write_audit("learn", {"status": "ok"})
    return state
