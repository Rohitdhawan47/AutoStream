import os
from langchain_ollama import ChatOllama

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

llm = ChatOllama(
    model="mistral:7b",
    temperature=0.3,
    base_url=OLLAMA_URL
)

# import google.generativeai as genai
# import os

# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# models = genai.list_models()
# for m in models:
#     print(m.name, m.supported_generation_methods)
