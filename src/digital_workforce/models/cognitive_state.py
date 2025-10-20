from pydantic import BaseModel
from typing import Any, Dict

class CognitiveState(BaseModel):
    inputs: Dict[str, Any]
    decision: Dict[str, Any] | None = None
    outcome: Dict[str, Any] | None = None
