from pydantic import BaseModel
from typing import Any, List, Dict

class DecisionResult(BaseModel):
    project_id: str
    action: str
    confidence: float
    explanation: str
    filters: List[Dict[str, Any]]
    roi_score: float = 0.0
