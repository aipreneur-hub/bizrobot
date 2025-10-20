import yaml, os
from jsonschema import validate

def load_yaml(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# Basic schema for decision templates
DECISION_SCHEMA = {
  "type": "object",
  "properties": {
    "project_id": {"type": "string"},
    "description": {"type": "string"},
    "version": {"type": ["string","null"]},
    "inputs": {"type": "array", "items": {"type": "string"}},
    "filters": {"type": "array", "items": {"type": "string"}},
    "decision_logic": {"type": "array"},
    "roi_metrics": {"type": "object"},
    "feedback_rules": {"type": "object"}
  },
  "required": ["project_id","inputs","filters","decision_logic"]
}

def load_decision_template(path: str) -> dict:
    data = load_yaml(path)
    validate(instance=data, schema=DECISION_SCHEMA)
    return data
