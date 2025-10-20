from typing import Dict, Any
from .registry import DecisionRegistry
from .filters_engine import FILTERS
from ..utils.expression_parser import eval_condition

class DecisionEvaluator:
    def __init__(self, registry: DecisionRegistry | None = None):
        self.registry = registry or DecisionRegistry()


    def decide(self, project_id, inputs):
        """
        Evaluate a decision project template with flexible filters.
        Supports both simple string filters and structured dict filters.
        """

        tpl = self.registry.load(project_id)
        filters = tpl.get("filters", [])
        logic = tpl.get("decision_logic", [])
        results = {}

        # ✅ Apply filters
        for f in filters:
            # Support both dicts and strings
            if isinstance(f, dict):
                filter_name = f.get("name")
            else:
                filter_name = f

            if not filter_name:
                continue  # skip invalid entries

            if filter_name not in FILTERS:
                print(f"⚠️  Unknown filter '{filter_name}', skipping.")
                continue

            try:
                passed, note = FILTERS[filter_name](inputs)
                results[filter_name] = {"passed": passed, "note": note}
            except Exception as e:
                print(f"❌ Error running filter {filter_name}: {e}")
                results[filter_name] = {"passed": False, "note": str(e)}

        # ✅ Execute decision logic
        decision_result = self.executor.execute(logic, inputs, results)
        return decision_result

