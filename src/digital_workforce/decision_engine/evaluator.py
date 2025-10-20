from digital_workforce.decision_engine.registry import DecisionRegistry
from digital_workforce.decision_engine.executor import DecisionExecutor
from digital_workforce.decision_engine.filters import FILTERS

class DecisionEvaluator:
    """Evaluates decision templates using defined filters and logic."""

    def __init__(self):
        self.registry = DecisionRegistry()
        self.executor = DecisionExecutor()  # ✅ FIX: ensure executor exists

    def decide(self, project_id, inputs):
        """
        Evaluate a decision project template with flexible filters.
        Supports both simple string filters and structured dict filters.
        """

        tpl = self.registry.load(project_id)
        filters = tpl.get("filters", [])
        logic = tpl.get("decision_logic", [])
        results = {}

        # ✅ Apply filters (support dict or string)
        for f in filters:
            if isinstance(f, dict):
                filter_name = f.get("name")
            else:
                filter_name = f

            if not filter_name:
                continue

            if filter_name not in FILTERS:
                print(f"⚠️  Unknown filter '{filter_name}', skipping.")
                continue

            try:
                passed, note = FILTERS[filter_name](inputs)
                results[filter_name] = {"passed": passed, "note": note}
            except Exception as e:
                print(f"❌ Error running filter {filter_name}: {e}")
                results[filter_name] = {"passed": False, "note": str(e)}

        # ✅ Execute the decision logic via the executor
        decision_result = self.executor.execute(logic, inputs, results)
        return decision_result
