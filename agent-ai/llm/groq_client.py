from langchain_groq import ChatGroq
from config import GROQ_API_KEY, MODEL_NAME, TEMPERATURE

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name=MODEL_NAME,
    temperature=TEMPERATURE
)
