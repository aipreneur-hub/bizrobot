from digital_workforce.decision_engine.executor import DecisionExecutor
from digital_workforce.decision_engine.filters import FILTERS

class DecisionEvaluator:
    def __init__(self, registry=None):
        self.registry = registry
        self.executor = DecisionExecutor()

    def decide(self, project_id, inputs):
        tpl = self.registry.load(project_id)
        filters = tpl.get("filters", [])
        logic = tpl.get("decision_logic", [])

        # Run filters
        for f in filters:
            func = FILTERS.get(f)
            if not func:
                print(f"⚠️  Unknown filter '{f}', skipping.")
                continue
            passed, note = func(inputs)
            if not passed:
                print(f"❌ Filter '{f}' failed: {note}")
                return {"status": "failed", "reason": note}

        # Execute logic
        results = {}
        decision_result = self.executor.execute(logic, inputs, results)
        return decision_result
