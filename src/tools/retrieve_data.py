from langchain_core.tools import tool
from memory.agent_memory import AgentMemory

from pydantic import BaseModel, Field

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
def retrieve_data(user_type,user_input):
    '''
    Retrieves information by the user for the particular attribute in core memory.

    Retrieve similar content, check if we have the answer if not add it as a prompt for llm
    Args:
        user_type: It can be either human or agent
        user_input: Question/Information requested by user
    '''
    return agent_memory.read_persistent_memory()

