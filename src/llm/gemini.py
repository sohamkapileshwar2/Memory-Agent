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

# Github reference - https://github.dev/langchain-ai/langchain-google/blob/main/libs/genai/langchain_google_genai/chat_models.py
class CustomChatGoogleGenerativeAI(ChatGoogleGenerativeAI):

    def _prepare_request(
        self,
        messages,
        *,
        stop,
        tools,
        functions,
        safety_settings,
        tool_config,
        tool_choice,
        generation_config,
        cached_content,
    ):
        request = super()._prepare_request(messages, stop=stop, tools=tools, functions=functions, safety_settings=safety_settings, tool_config=tool_config, tool_choice=tool_choice, generation_config=generation_config, cached_content=cached_content)

        print("RAW REQUEST BODY", request)

        return request
    
    def _generate(
        self,
        messages,
        stop,
        run_manager,
        *,
        tools,
        functions,
        safety_settings,
        tool_config,
        generation_config,
        cached_content,
        tool_choice,
        **kwargs,
    ):
        response = super()._generate(messages, stop, run_manager,tools=tools,functions=functions,safety_settings=safety_settings,tool_config=tool_config,generation_config=generation_config,cached_content=cached_content,tool_choice=tool_choice,kwargs=kwargs)

        print("PARSED RESPONSE", response)

        return response
    
    async def _agenerate(
        self,
        messages,
        stop,
        run_manager,
        *,
        tools,
        functions,
        safety_settings,
        tool_config,
        generation_config,
        cached_content,
        tool_choice,
        **kwargs,
    ):
        response = super()._agenerate(messages, stop, run_manager,tools=tools,functions=functions,safety_settings=safety_settings,tool_config=tool_config,generation_config=generation_config,cached_content=cached_content,tool_choice=tool_choice,kwargs=kwargs)

        print("PARSED ASYNC RESPONSE", response)

        return response
    

gemini = CustomChatGoogleGenerativeAI(model="gemini-2.0-flash",temperature=0,max_tokens=None,timeout=30,max_retries=2,callbacks=[CustomHandler()])