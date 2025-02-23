import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

# Setup environment variables
load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash",temperature=0,max_tokens=None,timeout=30,max_retries=2)


messages = [
    (
        "system",
        "You are a helpful assistant that translates English to French. Translate the user sentence.",
    ),
    ("human", "I love programming."),
]
ai_msg = llm.invoke(messages)
print(ai_msg)
