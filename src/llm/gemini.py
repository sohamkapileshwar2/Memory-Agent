import os
from dotenv import load_dotenv
from langchain_core.callbacks.base import BaseCallbackHandler
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import tools

# Setup environment variables
load_dotenv()

class CustomHandler(BaseCallbackHandler):
    def on_llm_start(
        self, serialized: dict[str, any], prompts: list[str], **kwargs: any
    ) -> any:
        formatted_prompts = "\n".join(prompts)
        # print(f"On LLM Start:\n{formatted_prompts}")
    
    # def on_tool_start( self, serialized: dict[str, any], input_str: str, **kwargs: any
    # ) -> any:
    #     formatted_prompts = "\n".join(input_str)
    #     print(f"On Tool start:\n{formatted_prompts}")

gemini = ChatGoogleGenerativeAI(model="gemini-2.0-flash",temperature=0,max_tokens=None,timeout=30,max_retries=2,callbacks=[CustomHandler()])