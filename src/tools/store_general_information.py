from langchain_core.tools import tool

from pydantic import BaseModel, Field
from memory.agent_memory import AgentMemory

# Store into memory tool call definition using pydantic class
# Used to pass definition of the function to LLM
class StoreGeneralInformation(BaseModel):
    '''
    Stores information inputed by the user for the particular attribute in core memory.

    Args:
        user_type: It can be either human or agent
        attribute: Attribute/Key name of the information of the user
        info: Information to be stored corresponsing to the attribute

    '''
    user_type: str = Field(description="Enum: human | agent")
    attribute: str = Field(description="Attribute name of the information being stored about the user type")
    info: str = Field(description="Information being stored corresponding to the attribute")

# Store into memory function implementation
def store_general_information(user_type:str, attribute:str, info:str,agent_memory:AgentMemory):
    '''
    Stores general information inputed by the user for the particular attribute in in-memory and other information in persistent memory.

    Args:
        user_type: It can be either human or agent
        attribute: Attribute/Key name of the information of the user
        info: Information to be stored corresponsing to the attribute
    '''
    general_information = agent_memory.general_information
    if user_type in general_information:
        general_information[user_type][attribute]=info
    else:
        general_information[user_type] = {}
        general_information[user_type][attribute]=info

    agent_memory.persist_general_information()

        

