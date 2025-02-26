import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from tools.store_into_memory import tool_calls

# Setup environment variables
load_dotenv()

gemini = ChatGoogleGenerativeAI(model="gemini-2.0-flash",temperature=0,max_tokens=None,timeout=30,max_retries=2)
gemini.bind_tools(tool_calls)