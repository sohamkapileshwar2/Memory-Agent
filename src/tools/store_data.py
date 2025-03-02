from langchain_core.tools import tool

from pydantic import BaseModel, Field
from memory.agent_memory import AgentMemory

# Store into memory tool call definition using pydantic class
# Used to pass definition of the function to LLM
class StoreData(BaseModel):
    '''
    Stores data which is inputed by the user for a particular topic in persistent memory.

    Args:
        topic_name: Topic of the information being stored
        info: Information to be stored corresponsing to the topic name
    '''
    topic_name: str = Field(description="Topic of the information being stored")
    info: str = Field(description="Information being stored corresponding ")

# Store into memory function implementation
def store_data(topic_name:str, info:str, agent_memory:AgentMemory):
    '''
    Stores data which is inputed by the user for a particular topic in persistent memory.

    Args:
        topic_name: Topic of the information being stored
        info: Information to be stored corresponsing to the topic name
    '''
    data = agent_memory.relevant_retrieved_memory
    if topic_name in data:
        data[topic_name].append(info)
    else:
        data[topic_name]=info

    agent_memory.persist_data()


        

