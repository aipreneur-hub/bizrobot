def compute_roi(tpl: dict, decision: str) -> float:
    # simple ROI: if decision is approve and template has cost_saved param
    base = tpl.get("roi_metrics", {}).get("cost_saved_per_auto_approval", 0.0)
    weight = tpl.get("roi_metrics", {}).get("accuracy_weight", 1.0)
    return float(base) * float(weight) if decision == "approve" else 0.0
