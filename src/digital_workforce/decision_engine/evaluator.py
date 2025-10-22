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

        # 🧩 Debug: print YAML content
        print("\n" + "="*60)
        print(f"🧠 Processing YAML for project: {project_id}")
        print("="*60)
        import yaml
        print(yaml.dump(tpl, sort_keys=False))
        print("="*60 + "\n")
        
        # Run filters
        for f in filters:
            # Handle both string and dict filter forms
            if isinstance(f, dict):
                filter_name = f.get("name")
            else:
                filter_name = f

            func = FILTERS.get(filter_name)
            if not func:
                print(f"⚠️  Unknown filter '{filter_name}', skipping.")
                continue

            passed, note = func(inputs)
            if not passed:
                print(f"❌ Filter '{filter_name}' failed: {note}")
                return {"status": "failed", "reason": note}

        # Execute logic
        results = {}
        decision_result = self.executor.execute(logic, inputs, results)
        return decision_result
