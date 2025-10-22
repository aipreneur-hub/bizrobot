from pydantic import BaseModel
from typing import Dict, Any

class ActionOutcome(BaseModel):
    status: str
    details: Dict[str, Any] | None = None
