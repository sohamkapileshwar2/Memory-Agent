from langchain.agents import Tool
from memory.agent_memory import AgentMemory

from pydantic.v1 import BaseModel, Field

# Retrieve from memory tool call definition using pydantic class
# Used to pass definition of the function to LLM
class RetrieveData(BaseModel):
    '''
    Retrieves information inputed by the user for the particular attribute in core memory.

    Args:
        user_type: It can be either human or agent
        user_input: Question/Information requested by user
    '''
    user_type: str = Field(description="Enum: human | agent")
    user_input: str = Field(description="Question/Information requested by user")

# retrieving complete memory for now
# Retrieve from memory function implementation
def retrieve_data(user_type, user_input, agent_memory):
    '''
    Retrieves data which is inputed by the user for a particular topic from persistent memory.
    
    Args:
        user_type: It can be either human or agent
        user_input: Question/Information requested by user
    '''
    return agent_memory.read_persistent_memory()


retrieve_data_tool = Tool(
    name="retrieve_data",
    description="Retrieves data which is inputed by the user for a particular topic from persistent memory.",
    func=retrieve_data,
)