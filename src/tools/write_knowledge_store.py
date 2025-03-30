from typing import Annotated, Optional, Type
from langchain.agents import Tool
from langchain_core.tools import InjectedToolArg
from langchain.tools import BaseTool

from pydantic.v1 import BaseModel, Field
from memory.agent_memory import AgentMemory

from langchain.callbacks.manager import (
	CallbackManagerForToolRun,
)

# Schema to pass to write knowledge store tool : Used to pass definition of the function to LLM
class WriteKnowledgeStore(BaseModel):
    topic_name: str = Field(description="Topic of the information being stored")
    info: str = Field(description="Information being stored corresponding ")
    agent_memory: Annotated[AgentMemory, InjectedToolArg] 
	
    class Config:
        arbitrary_types_allowed = True

class WriteKnowledgeStoreTool(BaseTool):

    name: str = "write_knowledge_store"
    description: str = """Stores user-provided knowledge into persistent memory when user provides information related to the topic.(e.g., notes, saved facts, code snippets, tech design)."""
    args_schema: Type[WriteKnowledgeStore] = WriteKnowledgeStore

    def _run(
        self,
        topic_name:str,
        info:str,
        agent_memory:AgentMemory,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> None:
        '''
        Stores user-provided knowledge into persistent memory when user provides information related to the topic. (e.g., notes, saved facts, code snippets, tech design).

        Args:
            topic_name: Topic of the information being stored
            info: Information to be stored corresponsing to the topic name
        '''
        write_knowledge_store(topic_name, info, agent_memory)

        
# Store into memory function implementation
def write_knowledge_store(topic_name:str, info:str, agent_memory:AgentMemory):
    data = agent_memory.retrieved_knowledge
    if topic_name in data:
        data[topic_name].append(info)
    else:
        data[topic_name]=info

    agent_memory.write_knowledge_store()

write_knowledge_store_tool = WriteKnowledgeStoreTool()