from typing import Annotated, Optional, Type
from langchain.agents import Tool
from langchain_core.tools import InjectedToolArg
from langchain.tools import BaseTool

from pydantic.v1 import BaseModel, Field
from memory.agent_memory import AgentMemory

from langchain.callbacks.manager import (
	CallbackManagerForToolRun,
)

class KnowledgeAttributes(BaseModel):
	knowledge_attribute_name: str = Field(description="Attribute(Key)of the information of the knowledge")
	knowledge_attribute_value: str = Field(description="Information(Value) to be stored corresponsing to the attribute")


# Schema to pass to write knowledge store tool : Used to pass definition of the function to LLM
class WriteKnowledgeStore(BaseModel):
    knowledge: list[KnowledgeAttributes] = Field(description="knowledge_attributes: List of KnowledgeAttributes")
    agent_memory: Annotated[AgentMemory, InjectedToolArg] 
	
    class Config:
        arbitrary_types_allowed = True

class WriteKnowledgeStoreTool(BaseTool):

    name: str = "write_knowledge_store"
    description: str = """Stores user-provided knowledge into persistent memory when user provides information related to the topic.(e.g., notes, saved facts, code snippets, tech design)."""
    args_schema: Type[WriteKnowledgeStore] = WriteKnowledgeStore

    def _run(
        self,
        knowledge: list,
        agent_memory:AgentMemory,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> None:
        '''
        Stores user-provided knowledge into persistent memory when user provides information related to the topic. (e.g., notes, saved facts, code snippets, tech design).

        Args:

            knowledge: List of KnowledgeAttributes

        '''
        write_knowledge_store(knowledge, agent_memory)

        
# Store into memory function implementation
def write_knowledge_store(knowledge:list, agent_memory:AgentMemory):
    data = agent_memory.retrieved_knowledge
    for info in knowledge:
        if info.knowledge_attribute_name in data:
            data[info.knowledge_attribute_name].append(info.knowledge_attribute_value)
        else:
            data[info.knowledge_attribute_name] = [info.knowledge_attribute_value]

    agent_memory.write_knowledge_store()

write_knowledge_store_tool = WriteKnowledgeStoreTool()