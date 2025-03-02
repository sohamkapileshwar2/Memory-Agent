from langchain_core.tools import tool

from pydantic import BaseModel, Field

# Store into memory tool call definition using pydantic class
# Used to pass definition of the function to LLM
class StoreIntoMemory(BaseModel):
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
def store_into_memory(user_type:str, attribute:str, info:str, agent_memory:dict):
    '''
    Stores information inputed by the user for the particular attribute in core memory.

    Args:
        user_type: It can be either human or agent
        attribute: Attribute/Key name of the information of the user
        info: Information to be stored corresponsing to the attribute
    '''
    if user_type in agent_memory:
        agent_memory[user_type][attribute]=info
    else:
        agent_memory[user_type] = {}
        agent_memory[user_type][attribute]=info

