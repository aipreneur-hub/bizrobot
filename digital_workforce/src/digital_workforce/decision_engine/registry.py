import os
from typing import Dict
from ..config import settings
from ..utils.yaml_loader import load_decision_template

class DecisionRegistry:
    """
    Generic loader for decision templates.
    External projects must set DECISIONS_PATH env var.
    """
    def __init__(self, base_dir: str | None = None):
        self.base_dir = base_dir or settings.decisions_dir
        self._cache: Dict[str, dict] = {}

    def load(self, project_id: str) -> dict:
        if project_id in self._cache:
            return self._cache[project_id]

        path = os.path.join(self.base_dir, f"{project_id}.yaml")
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Decision template not found: {path}\n"
                f"Set DECISIONS_PATH env variable for your templates."
            )
        tpl = load_decision_template(path)
        self._cache[project_id] = tpl
        return tpl
