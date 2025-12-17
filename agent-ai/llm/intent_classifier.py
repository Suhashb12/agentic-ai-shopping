from langchain_core.prompts import PromptTemplate
from llm.groq_client import get_llm
import json


INTENT_PROMPT = PromptTemplate(
    input_variables=["input"],
    template="""
You are an expert shopping assistant with 10+ years of experience.

Analyze the user query and extract intent in STRICT JSON format.

Rules:
- Do NOT add explanations
- Do NOT add extra text
- Output ONLY valid JSON

JSON schema:
{{
  "category": "mobile | laptop | tv | cosmetics | fashion | other",
  "budget": number | null,
  "features": [string],
  "intent": "product_search | comparison | recommendation | other"
}}

User query:
"{input}"
"""
)


def classify_intent(user_input: str) -> dict:
    """
    Classifies user intent using Groq LLM via LangChain.
    Always returns a safe dictionary.
    """

    llm = get_llm()  # lazy, config-aware

    prompt = INTENT_PROMPT.format(input=user_input)

    try:
        response = llm.invoke(prompt)
        raw = response.content.strip()

        data = json.loads(raw)

        # normalize
        return {
            "category": data.get("category", "other"),
            "budget": data.get("budget"),
            "features": data.get("features", []),
            "intent": data.get("intent", "other"),
        }

    except Exception as e:
        print("❌ Intent classification failed:", e)
        return {
            "category": "other",
            "budget": None,
            "features": [],
            "intent": "other"
        }
