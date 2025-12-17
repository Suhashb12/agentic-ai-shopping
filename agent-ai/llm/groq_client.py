# llm/groq_client.py
from langchain_groq import ChatGroq
from config import GROQ_API_KEY

_llm = None  # lazy singleton

def get_llm():
    global _llm

    if _llm is None:
        if not GROQ_API_KEY:
            raise RuntimeError(
                "GROQ_API_KEY is missing. Set it in environment before starting the app."
            )

        _llm = ChatGroq(
            model="llama-3.1-8b-instant",
            api_key=GROQ_API_KEY,
            temperature=0.4
        )

    return _llm
