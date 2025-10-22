"""
Router: classify intent + extract entities (LLM).
"""
from typing import Dict, Any
import json
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

class Router:
    def __init__(self, llm=None):
        self.llm = llm or ChatOpenAI(model="gpt-4o-mini", temperature=0)

    def route(self, user_input: str) -> Dict[str, Any]:
        prompt = ChatPromptTemplate.from_template("""
        You classify user input for a business agent.

        Return ONLY JSON:
        {{
          "intent": "Command" | "Decision" | "Question",
          "entities": [string],
          "confidence": 0.0
        }}

        Input: "{user_input}"
        """)
        raw = self.llm.invoke(prompt.format(user_input=user_input)).content
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {"intent": "Command", "entities": [], "confidence": 0.5, "raw": raw}
