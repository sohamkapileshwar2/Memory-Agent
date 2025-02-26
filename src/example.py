from llm.gemini import gemini
from memory.core_memory import agent_memory

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

ai_msg = gemini.invoke(messages)
print(ai_msg)
print("\n\n\n")
print("CONTENT", ai_msg.content)
print("AGENT MEMORY", agent_memory)