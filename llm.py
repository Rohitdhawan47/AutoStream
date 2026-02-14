import os
from langchain_ollama import ChatOllama

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

llm = ChatOllama(
    model="mistral:7b",
    temperature=0.3,
    base_url=OLLAMA_URL
)
