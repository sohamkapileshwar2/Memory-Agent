from llm.gemini import gemini_with_tools
from memory.core_memory import agent_memory
from tools.store_into_memory import store_into_memory


system_prompt = "You are a chatbot. " \
+ "You have a section of your context called [MEMORY] " \
+ "that contains information relevant to your conversation. "\
+ "Store all relevant information about the user by calling the tool (store_into_memory). "

messages = [
    (
        "system",
        system_prompt,
    ),
    ("human", "I love programming."),
]

gemini_response = gemini_with_tools.invoke(messages)

tool_call = gemini_response.tool_calls[0]
tool_output = {"store_into_memory": store_into_memory}[tool_call["name"].lower()].invoke(tool_call["args"])

print(agent_memory)