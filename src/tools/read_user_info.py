from typing import Annotated, Optional, Type
from langchain.agents import Tool
from memory.agent_memory import AgentMemory
from langchain_core.tools import InjectedToolArg
from langchain.tools import BaseTool

from pydantic.v1 import BaseModel, Field

from langchain.callbacks.manager import (
	CallbackManagerForToolRun,
)
# Retrieve from memory tool call definition using pydantic class
# Used to pass definition of the function to LLM
class ReadUserInfo(BaseModel):
    '''
    Retrieves user related information inputed by the user for the particular attribute in core memory.

    Args:
        user_type: It can be either human or agent
        user_input: Question/Information requested by user
    '''
    user_type: str = Field(description="Enum: human | agent")
    user_input: str = Field(description="Question/Information requested by user")
    agent_memory: Annotated[AgentMemory, InjectedToolArg] 
	
    class Config:
        arbitrary_types_allowed = True

class ReadUserInfoTool(BaseTool):

    name: str = "retrieve_generak_information"
    description: str = """Retrieves user related information which is inputed by the user for a particular topic from persistent memory."""
    args_schema: Type[ReadUserInfo] = ReadUserInfo


    def _run(
        self,
        user_type:str,
        user_input:str,
        agent_memory:AgentMemory,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> None:
        '''
        Retrieves user related information which is inputed by the user for a particular topic from persistent memory.
        
        Args:
            user_type: It can be either human or agent
            user_input: Question/Information requested by user
        '''
        read_user_info(user_type, user_input, agent_memory
    )

# retrieving complete memory for now
# Retrieve from memory function implementation
def read_user_info(user_type, user_input, agent_memory):
    return agent_memory.read_general_information()

read_user_info_tool = ReadUserInfoTool()