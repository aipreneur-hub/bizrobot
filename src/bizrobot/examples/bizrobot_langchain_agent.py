from bizrobot.core.router import Router
from bizrobot.core.planner import Planner
from bizrobot.core.compiler import TaskCompiler
from bizrobot.core.executor import Executor

def main():
    user_input = "Register a new employee with SSK insurance and Luca"

    router = Router()
    planner = Planner()
    compiler = TaskCompiler()
    executor = Executor()

    route = router.route(user_input)
    print("Route:", route)

    plan = planner.create_plan(user_input, route)
    print("Plan:", plan)

    dsl = compiler.compile_plan(plan)
    print(dsl)

    results = executor.execute(dsl)
    print("Results:", results)

if __name__ == "__main__":
    main()
