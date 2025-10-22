from core.compiler.compiler import compile_to_dsl
def test_compile_attaches_budgets(registry, policies, plan):
    dsl = compile_to_dsl(plan, registry, policies, "run-1")
    assert dsl.budget["max_cost_usd"] > 0
