from langchain_core.prompts import PromptTemplate
from llm.groq_client import llm
import json

prompt = PromptTemplate(
    template="""
Classify the user intent into one of:
DISCOVER, COMPARE, BUDGET, ORDER, COMPLAINT

Respond ONLY in JSON:
{{"intent": "<intent>"}}

User message:
{input}
""",
    input_variables=["input"]
)

def classify_intent(text):
    res = llm.invoke(prompt.invoke({"input": text}))
    try:
        return json.loads(res.content)
    except:
        return {"intent": "DISCOVER"}
