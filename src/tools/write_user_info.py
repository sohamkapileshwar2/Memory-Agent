from langchain.agents import Tool
from langchain.tools import BaseTool
from langchain_core.tools import InjectedToolArg

from pydantic.v1 import BaseModel, BaseSettings, Field
from typing import Annotated,Type,Optional
from memory.agent_memory import AgentMemory

from langchain.callbacks.manager import (
	CallbackManagerForToolRun,
)

# Store into memory tool call definition using pydantic class
# Used to pass definition of the function to LLM
class WriteUserInformation(BaseModel):
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
	agent_memory: Annotated[AgentMemory, InjectedToolArg] 
	
	class Config:
		arbitrary_types_allowed = True

class WriteUserInformationTool(BaseTool):

	name: str = "write_user_info"
	description: str = """Writes user related information for the particular attribute in persistent memory."""
	args_schema: Type[WriteUserInformation] = WriteUserInformation
  
	def _run(
		self,
		user_type:str,
		attribute:str,
		info:str,
		agent_memory:AgentMemory,
		run_manager: Optional[CallbackManagerForToolRun] = None,
	) -> None:
		'''
		Writes user information inputed by the user for the particular attribute in persistent memory.

		Args:
			user_type: Enum - human | agent
			attribute: Attribute/Key name of the information of the user
			info: Information to be stored corresponsing to the attribute
		'''
		write_user_info(user_type, attribute, info, agent_memory)

# Store into memory function implementation
def write_user_info(user_type:str, attribute:str, info:str, agent_memory:AgentMemory):
	user_info = agent_memory.user_info
	if user_type in user_info:
		user_info[user_type][attribute]=info
	else:
		user_info[user_type] = {}
		user_info[user_type][attribute]=info

	agent_memory.persist_user_info()

write_user_info_tool = WriteUserInformationTool()
