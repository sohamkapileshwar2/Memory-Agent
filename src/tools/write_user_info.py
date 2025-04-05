from langchain.agents import Tool
from langchain.tools import BaseTool
from langchain_core.tools import InjectedToolArg

from pydantic.v1 import BaseModel, BaseSettings, Field
from typing import Annotated,Type,Optional
from memory.agent_memory import AgentMemory

from langchain.callbacks.manager import (
	CallbackManagerForToolRun,
)

class UserProfileAttributes(BaseModel):
	user_attribute_name: str = Field(description="Attribute(Key)of the information of the user")
	user_attribute_value: str = Field(description="Information(Value) to be stored corresponsing to the attribute")

# Store into memory tool call definition using pydantic class
# Used to pass definition of the function to LLM
class WriteUserInformation(BaseModel):
	user_type: str = Field(description="Enum: human | agent")
	user_profile: list[UserProfileAttributes] = Field(description="user_profile: List of UserProfileAttributes")
	agent_memory: Annotated[AgentMemory, InjectedToolArg] 
	
	class Config:
		arbitrary_types_allowed = True

class WriteUserInformationTool(BaseTool):

	name: str = "write_user_info"
	description: str = """Stores user-related information into persistent memory. (e.g., name, preferences, personal details)."""
	args_schema: Type[WriteUserInformation] = WriteUserInformation
  
	def _run(
		self,
		user_type:str,
		user_profile:list,
		agent_memory:AgentMemory,
		run_manager: Optional[CallbackManagerForToolRun] = None,
	) -> None:
		'''
		Writes user-related information inputed by the user for the particular attribute in persistent memory.(e.g., name, preferences, personal details).

		Args:
			user_type: Enum - human | agent
			user_profile: List of UserProfileAttributes
		'''
		write_user_info(user_type, user_profile, agent_memory)

# TODO: Need to implement multiple user attributes input into the file
# Store into memory function implementation
def write_user_info(user_type:str, user_profile:list , agent_memory:AgentMemory):
	user_info = agent_memory.user_info
	if user_type in user_info:
		for profile in user_profile:
			# append user_profile to the existing user_info
			user_info[user_type].update({profile.user_attribute_name : profile.user_attribute_value})
	else:
		user_info[user_type] = {}
		for profile in user_profile:
			# append user_profile to the existing user_info
			user_info[user_type].update({profile.user_attribute_name : profile.user_attribute_value})

	agent_memory.write_user_info()

write_user_info_tool = WriteUserInformationTool()
