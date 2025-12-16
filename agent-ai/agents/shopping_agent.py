from langchain_core.prompts import PromptTemplate
from llm.groq_client import llm

prompt = PromptTemplate(
    template=open("prompts/system.txt").read() +
             open("prompts/shopping_agent.txt").read(),
    input_variables=["input"]
)

def handle_shopping(text):
    return llm.invoke(prompt.format(input=text)).content
