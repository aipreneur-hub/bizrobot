from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Settings:
    env: str = os.getenv("DW_ENV", "dev")
    project_dir: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    decisions_dir: str = os.getenv("DECISIONS_PATH", os.path.join(os.path.dirname(__file__), "decision_engine", "decision_projects"))

settings = Settings()
