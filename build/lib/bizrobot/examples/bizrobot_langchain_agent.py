# bizrobot/examples/bizrobot_langchain_agent.py
from src.services.orchestrator.agent_graph import BizRobotAgent

if __name__ == "__main__":
    agent = BizRobotAgent()
    command = "Register a new employee with SSK insurance and Luca"
    output = agent.run(command)
    print("\n✅ Final Output:")
    print(output)
