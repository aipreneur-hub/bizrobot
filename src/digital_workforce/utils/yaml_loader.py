import yaml
from jsonschema import validate

def load_yaml(path: str) -> dict:
    """Safely load a YAML file into a Python dictionary."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# ✅ Enhanced schema to support structured filters and flexible inputs
DECISION_SCHEMA = {
    "type": "object",
    "properties": {
        "project_id": {"type": "string"},
        "description": {"type": ["string", "null"]},
        "version": {"type": ["string", "null"]},

        # Inputs: either a list of strings or list of objects
        "inputs": {
            "type": "array",
            "items": {
                "oneOf": [
                    {"type": "string"},
                    {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "type": {"type": "string"},
                            "required": {"type": "boolean"}
                        },
                        "required": ["name"]
                    }
                ]
            }
        },

        # ✅ Fix: allow structured filter objects instead of plain strings
        "filters": {
            "type": "array",
            "items": {
                "oneOf": [
                    {"type": "string"},
                    {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "type": {"type": "string"},
                            "required": {"type": "boolean"}
                        },
                        "required": ["name"]
                    }
                ]
            }
        },

        # Decision logic must be an array of steps
        "decision_logic": {"type": "array"},

        "roi_metrics": {"type": ["object", "null"]},
        "feedback_rules": {"type": ["object", "null"]}
    },
    "required": ["project_id", "inputs", "filters", "decision_logic"]
}

def load_decision_template(path: str) -> dict:
    """Load and validate a decision template YAML file."""
    data = load_yaml(path)
    try:
        validate(instance=data, schema=DECISION_SCHEMA)
    except Exception as e:
        raise ValueError(f"❌ Validation failed for {path}: {e}")
    return data
