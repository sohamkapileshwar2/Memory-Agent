from llm.gemini import gemini_with_tools
from memory.core_memory import agent_memory
from tools.store_into_memory import store_into_memory
from langchain.globals import set_debug, set_verbose

from llm.gemini import gemini_with_tools
from tools import tools, tool_calls
from memory.core_memory import AgentMemory


set_debug(True)
set_verbose(True)

agent_memory = AgentMemory()

system_prompt = f"""You are a chatbot.
You have a section of your context called [CORE MEMORY] that contains information relevant to your conversation. Its a JSON containing personal information about the user and their stored data.
You have two tasks to perform:
    1. If the user gives any information about them or asks you to remember some text, you have to store it in your persistent memory. Acknowledge the user that you have stored the information in memory.
    2. If the user asks a query/question, then either answer the query if the information is available in your [CORE MEMORY] or retrieve the most relevant information from your persistent memory, and use that as your context to reply back to the user.
You have the following available tools to call to perform the above tasks:
    1. StoreIntoMemory - Tool to store any information into persistent memory
    2. RetrieveFromMemory - Tool to retrieve information from persistent memory

```[CORE MEMORY]
{agent_memory.core_memory}
```
"""

messages = [
    (
        "system",
        system_prompt,
    ),
    ("human", "When did i write my first program?"),
]

# Model Invocation

chain = gemini_with_tools
response = chain.invoke(messages)

print("RESPONSE", type(response), response, end="\n\n")
print("TOOL CALLS", type(response.tool_calls), response.tool_calls, end="\n\n")

# Invoke tools
model_tool_calls = response.tool_calls
for tool_call in model_tool_calls:
    function = tool_calls.get(tool_call["name"])
    if function:
        try:
            function(**tool_call["args"], agent_memory=agent_memory.core_memory)
            print(f"Function {function.__str__()} called successfully with arguments {tool_call["args"]}", end="\n\n")
            print(f"Agent Memory : {agent_memory.core_memory}", end="\n\n")
            
            agent_memory.persist_agent_memory()
        except:
            print(f"Exception while calling {function.__str__()}", end="\n\n")