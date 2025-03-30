from typing import Annotated, Optional, Type
from langchain.agents import Tool
from memory.agent_memory import AgentMemory
from langchain_core.tools import InjectedToolArg
from langchain.tools import BaseTool

from pydantic.v1 import BaseModel, Field

from langchain.callbacks.manager import (
	CallbackManagerForToolRun,
)
# Pydantic class: schema argument for read user info tool call
class ReadUserInfo(BaseModel):
    user_type: str = Field(description="Enum: human | agent")
    user_input: str = Field(description="Question/Information requested by user")
    agent_memory: Annotated[AgentMemory, InjectedToolArg] 
	
    class Config:
        arbitrary_types_allowed = True

class ReadUserInfoTool(BaseTool):

    name: str = "read_user_info"
    description: str = """Retrieve user related information from persistent memory if it is not present in prompt context.(e.g., name, preferences, personal details)."""
    args_schema: Type[ReadUserInfo] = ReadUserInfo


    def _run(
        self,
        user_type:str,
        user_input:str,
        agent_memory:AgentMemory,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict:
        '''
        Retrieve user related information from persistent memory if it is not present in prompt context .(e.g., name, preferences, personal details).
        
        Args:
            user_type: It can be either human or agent
            user_input: Question/Information requested by user
        '''
        return read_user_info(user_type, user_input, agent_memory)

def read_user_info(user_type, user_input, agent_memory):
    agent_memory.read_user_info()

    return agent_memory.user_info

read_user_info_tool = ReadUserInfoTool()