from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    temperature=0.3
)
# import google.generativeai as genai
# import os

# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# models = genai.list_models()
# for m in models:
#     print(m.name, m.supported_generation_methods)
