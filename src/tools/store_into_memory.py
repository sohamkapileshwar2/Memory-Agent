from langchain_core.tools import tool
from memory.core_memory import agent_memory

@tool
def store_into_memory(user_type:str, attribute:str, info:str):
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

tool_calls = [store_into_memory]


