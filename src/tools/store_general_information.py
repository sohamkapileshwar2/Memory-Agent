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
	agent_memory: Annotated[AgentMemory, InjectedToolArg] 
	
	class Config:
		arbitrary_types_allowed = True

class StoreGeneralInformationTool(BaseTool):

	name: str = "store_general_information"
	description: str = """Stores general information inputed by the user for the particular attribute in persistent memory."""
	args_schema: Type[StoreGeneralInformation] = StoreGeneralInformation
  
	def _run(
		self,
		user_type:str,
		attribute:str,
		info:str,
		agent_memory:AgentMemory,
		run_manager: Optional[CallbackManagerForToolRun] = None,
	) -> None:
		'''
		Stores general information inputed by the user for the particular attribute in persistent memory.

		Args:
			user_type: Enum - human | agent
			attribute: Attribute/Key name of the information of the user
			info: Information to be stored corresponsing to the attribute
		'''
		store_general_information(user_type, attribute, info, agent_memory)

store_general_information_tool = StoreGeneralInformationTool()

# Store into memory function implementation
def store_general_information(user_type:str, attribute:str, info:str, agent_memory:AgentMemory):
	'''
	Stores general information inputed by the user for the particular attribute in persistent memory.

	Args:
		user_type: Enum - human | agent
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

# store_general_information_tool = Tool(
# 	name="store_general_information",
# 	description="Stores general information inputed by the user for the particular attribute in persistent memory.",
# 	func=store_general_information,
# 	args_schema=StoreGeneralInformation,
# )

