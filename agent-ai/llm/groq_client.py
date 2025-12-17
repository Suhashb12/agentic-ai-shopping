from langchain_groq import ChatGroq
from config import GROQ_API_KEY

# -----------------------------
# Private singleton instance
# -----------------------------
_llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.1-8b-instant",
    temperature=0.4,
)

# -----------------------------
# Public access patterns
# -----------------------------

# 1️⃣ Direct import style
llm = _llm

# 2️⃣ Factory-style access (used by some agents)
def get_llm():
    return _llm
