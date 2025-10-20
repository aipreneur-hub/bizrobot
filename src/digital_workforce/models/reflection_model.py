from pydantic import BaseModel

class ReflectionReport(BaseModel):
    learned: bool = False
    note: str = "ok"
