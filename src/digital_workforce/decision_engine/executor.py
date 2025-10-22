import jinja2

class DecisionExecutor:
    """
    Executes the decision logic steps defined in the YAML.
    Supports sequential actions and conditional decisions.
    """

    def __init__(self):
        self.env = jinja2.Environment()

    def execute(self, steps, inputs, results):
        context = {**inputs, **results}
        last_decision = None

        for step in steps:
            # Handle named step
            if "name" in step and "action" in step:
                name = step["name"]
                action = step["action"]
                args = self._render_args(step.get("args", {}), context)

                # For now, mock skill execution
                print(f"⚙️  Running skill: {action}({args})")
                context[name] = {"result": f"Executed {action}"}

            # Handle decision blocks
            elif "decision" in step:
                decision_block = step["decision"]
                condition = decision_block.get("if")
                condition_result = self._evaluate_condition(condition, context)

                if condition_result:
                    last_decision = decision_block["then"]["decision"]
                else:
                    last_decision = decision_block["else"]["decision"]

                context["decision"] = last_decision
                print(f"🧠 Decision made: {last_decision}")

        return {"context": context, "decision": last_decision}

    def _render_args(self, args, context):
        """Render Jinja-style templates inside args."""
        rendered = {}
        for k, v in args.items():
            if isinstance(v, str) and "{{" in v:
                rendered[k] = self.env.from_string(v).render(context)
            else:
                rendered[k] = v
        return rendered

    def _evaluate_condition(self, condition, context):
        """Safely evaluate basic logical expressions."""
        try:
            expr = self.env.from_string(f"{{% if {condition} %}}True{{% else %}}False{{% endif %}}")
            return expr.render(context) == "True"
        except Exception as e:
            print(f"⚠️  Error evaluating condition '{condition}': {e}")
            return False
