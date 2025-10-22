"""
Planner: NL goal -> ordered steps (LLM) with JSON fence cleaning.
"""
from typing import Dict, Any
import json, re
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

class Planner:
    def __init__(self, llm=None):
        self.llm = llm or ChatOpenAI(model="gpt-4o-mini", temperature=0)

    def create_plan(self, user_input: str, route_result: Dict[str, Any]) -> Dict[str, Any]:
        intent = route_result.get("intent", "Command")
        entities = route_result.get("entities", [])

        prompt = ChatPromptTemplate.from_template("""
        Decompose the goal into ordered steps for a business agent.
        Constraints:
        - Use actions from: ["call_api","web.fill_form","file.generate","extract_data","analyze","notify"].
        - Each step: id (int), action (string), target (string), description (string).

        Return ONLY JSON like:
        {{
          "goal": "...",
          "plan": [{{"id":1,"action":"call_api","target":"SSK","description":"..."}}]
        }}

        Goal: "{user_input}"
        Intent: "{intent}"
        Entities: {entities}
        """)
        raw = self.llm.invoke(prompt.format(user_input=user_input, intent=intent, entities=entities)).content

        # Strip markdown code fences if present
        clean = re.sub(r"^```(json)?|```$", "", raw.strip(), flags=re.MULTILINE).strip()
        try:
            return json.loads(clean)
        except json.JSONDecodeError:
            return {"goal": user_input, "plan": [], "raw_output": raw}
