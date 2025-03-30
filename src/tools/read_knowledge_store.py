from typing import Annotated, Optional, Type
from langchain.agents import Tool
from memory.agent_memory import AgentMemory
from langchain_core.tools import InjectedToolArg
from langchain.tools import BaseTool

from pydantic.v1 import BaseModel, Field

from langchain.callbacks.manager import (
	CallbackManagerForToolRun,
)
# Pydantic class: schema argument for read knowledge store tool call
class ReadKnowledgeStore(BaseModel):
    user_type: str = Field(description="Enum: human | agent")
    user_input: str = Field(description="Question/Information requested by user")
    agent_memory: Annotated[AgentMemory, InjectedToolArg] 
	
    class Config:
        arbitrary_types_allowed = True

class ReadKnowledgeStoreTool(BaseTool):

    name: str = "read_knowledge_store"
    description: str = """Retrieve user-provided knowledge from persistent memory when user asks a question related to the topic if it is not present in prompt context. eg. (e.g., notes, saved facts, code snippets, tech design)."""
    args_schema: Type[ReadKnowledgeStore] = ReadKnowledgeStore


    def _run(
        self,
        user_type:str,
        user_input:str,
        agent_memory:AgentMemory,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict:
        '''
        Retrieve user-provided knowledge from persistent memory when user asks a question related to the topic if it is not present in prompt context. eg. (e.g., notes, saved facts, code snippets, tech design).
        
        Args:
            user_type: It can be either human or agent
            user_input: Question/Information requested by user
        '''
        return read_knowledge_store(user_type, user_input, agent_memory)


def read_knowledge_store(user_type, user_input, agent_memory):
    agent_memory.read_knowledge_store()

    return agent_memory.retrieved_knowledge

read_knowledge_store_tool = ReadKnowledgeStoreTool()