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
class ReadKnowledgeStore(BaseModel):
    '''
    Retrieves knowledge store inputed by the user for the particular attribute in core memory.

    Args:
        user_type: It can be either human or agent
        user_input: Question/Information requested by user
    '''
    user_type: str = Field(description="Enum: human | agent")
    user_input: str = Field(description="Question/Information requested by user")
    agent_memory: Annotated[AgentMemory, InjectedToolArg] 
	
    class Config:
        arbitrary_types_allowed = True

class ReadKnowledgeStoreTool(BaseTool):

    name: str = "read_knowledge_store"
    description: str = """Retrieves data which is inputed by the user for a particular topic from persistent memory."""
    args_schema: Type[ReadKnowledgeStore] = ReadKnowledgeStore


    def _run(
        self,
        user_type:str,
        user_input:str,
        agent_memory:AgentMemory,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict:
        '''
        Retrieves knowledge store which is inputed by the user for a particular topic from persistent memory.
        
        Args:
            user_type: It can be either human or agent
            user_input: Question/Information requested by user
        '''
        return read_knowledge_store(user_type, user_input, agent_memory)

# retrieving complete memory for now
# Retrieve from memory function implementation
def read_knowledge_store(user_type, user_input, agent_memory):
    agent_memory.read_knowledge_store()

    return agent_memory.retrieved_knowledge

read_knowledge_store_tool = ReadKnowledgeStoreTool()