# bizrobot/services/orchestrator/agent_graph.py
from bizrobot.core.router.router import Router
from bizrobot.core.planner.planner import Planner
from bizrobot.core.compiler.compiler import TaskCompiler
from bizrobot.core.executor.executor import Executor
from bizrobot.core.critic.critic import Critic
from bizrobot.core.policy.engine import PolicyEngine
from bizrobot.core.registry.cap_registry import CapabilityRegistry
from bizrobot.core.observability.events import EventBus

class BizRobotAgent:
    """Orchestrates Router → Planner → Compiler → Executor → Critic pipeline."""
    def __init__(self):
        self.registry = CapabilityRegistry("bizrobot/core/registry/capabilities")
        self.router = Router()
        self.planner = Planner(self.registry)
        self.compiler = TaskCompiler()
        self.executor = Executor()
        self.critic = Critic()
        self.policy = PolicyEngine()
        self.events = EventBus()

    def run(self, user_input: str):
        self.events.emit("input", {"text": user_input})
        route = self.router.route(user_input)
        self.events.emit("router", route)

        plan_json = self.planner.plan(user_input)
        self.events.emit("plan", plan_json)

        dsl_json = self.compiler.compile(plan_json)
        self.events.emit("compiled", dsl_json)

        if not self.policy.check(dsl_json):
            raise Exception("Policy check failed")

        results = self.executor.execute(dsl_json)
        reviewed = self.critic.review(results)
        self.events.emit("results", reviewed)
        return reviewed
