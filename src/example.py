from llm.gemini import gemini_with_tools
from langchain.globals import set_debug, set_verbose
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage

from llm.gemini import gemini_with_tools
from tools import tools, tool_calls
from memory.agent_memory import AgentMemory
import logging


set_debug(True)
set_verbose(True)

logging.basicConfig(level=logging.DEBUG)  # Set logging level to DEBUG


agent_memory = AgentMemory()

def generate_system_prompt(general_information: dict, relevant_retrieved_memory:dict):
    return f"""You are a chatbot.
        You have the following tools available for your use:
            1. StoreGeneralInformation : Stores general information about the user like their name, gender, date of birth etc.
            2. StoreData : Stores data related to any topic that the user is inputting.
            3. RetrieveData : Retrieves data corresponding to a specific topic.
        Your task is to chat with the user. If the user gives or asks any particular information, then you can also use any appropriate tool,
        to either store information about the user or retrieve information about the user. 
        """
        
        
        # f"""You are a chatbot.
        # You have two sections in your context one called [GENERAL INFORMATION] that contains information relevant to your conversation. Its a JSON containing personal information about the user and their stored data.
        # The other called [RELEVANT RETRIEVED MEMORY] which contains retrieved information from persistent memory related to user's question.
        # You have these tasks to perform:
        #     1. If the user gives any information about them or asks you to remember some text, you have to store it in your persistent memory. Acknowledge the user that you have stored the information in memory.
        #     2. If the user asks a query/question, answer the query if the information is available in your [GENERAL INFORMATION]
        #     3. If the user asks a query/question, answer the query if the information is available in your [RELEVANT RETRIEVED MEMORY]
        #     4. If the user asks a query/question and the answer is not available in the above two tasks, retrieve the most relevant information from your persistent memory and then answer thier question.
        # You have the following available tools to call to perform the above tasks:
        #     1. StoreGeneralInformation : Stores general information about the user like their name, gender, date of birth etc.
        #     2. StoreData : Stores data related to any topic that the user is inputting.
        #     3. RetrieveData : Retrieves data corresponding to a specific topic
        # You do not have to do tool call everytime. Once tool call is executed successfully, respond back to the user.

        # ```[GENERAL INFORMATION]
        # {general_information}
        # ```

        # ```[RELEVANT RETRIEVED MEMORY]
        # {relevant_retrieved_memory}
        # ```
        # """
messages = []

def agent_step(user_input):
    system_message = ("system", generate_system_prompt(agent_memory.general_information, agent_memory.relevant_retrieved_memory))
    human_message = ("human", user_input)
    messages.append(system_message)
    messages.append(human_message)

    chain = gemini_with_tools
    
    while True:
        
        # Model Invocation
        response = chain.invoke(messages)

        print("RESPONSE", type(response), response, end="\n\n")
        print("TOOL CALLS", type(response.tool_calls), response.tool_calls, end="\n\n")

        if response.content:
            messages.append({
                "role": "assistant", 
                "content": f"{response.content}"
            })

        # if NOT calling a tool (responding to the user), return 
        if not response.tool_calls: 
            return response.content
        
        # Invoke tools
        model_tool_calls = response.tool_calls
        for tool_call in model_tool_calls:
            function = tool_calls.get(tool_call["name"])
            if function:
                try:
                    function(**tool_call["args"], agent_memory=agent_memory)
                    print(f"Function {function.__str__()} called successfully with arguments {tool_call['args']}", end="\n\n")
                    print(f"Agent Memory : {agent_memory.general_information}", end="\n\n")
                    messages.append({
                        "role": "tool", 
                        "tool_call_id": tool_call["id"], 
                        "name": tool_call["name"], 
                        "content": f"Tool {tool_call["name"]} with id {tool_call["id"]} executed successfully."
                    })
                except Exception:
                    print(f"Exception while calling {function.__str__()}", end="\n\n")
                    return Exception

# while True:
#     user_input = input("Hi there! I'm here to serve you. Please tell me how can I help you?\n") 
#     print(agent_step(user_input))


# Test
messages.append(SystemMessage(content=f"""You are a chatbot.
        You have the following tools available for your use:
            1. StoreGeneralInformation : Stores general information about the user like their name, gender, date of birth etc.
            2. StoreData : Stores data related to any topic that the user is inputting.
        Your task is to chat with the user. If the user gives any particular information, then you can also use any appropriate tool,
        to either store information about the user or any relevant data they give. If the user asks a question, try to check for the answer in your chat history and respond back. 
        """))

messages.append(HumanMessage(content="Hello my name is soham. I like playing football"))

model = gemini_with_tools
response = model.invoke(messages)
print("RESPONSE", type(response), response, end="\n\n")
print("TOOL CALLS", type(response.tool_calls), response.tool_calls, end="\n\n")

if response.content:    
    messages.append(AIMessage(content=response.content))

messages.append(AIMessage(content="I have stored your name and that you like to play football."))

for tool in response.tool_calls:
    messages.append(ToolMessage(tool_call_id=tool["id"], content="", status="success"))


messages.append(HumanMessage(content="Hey which sport do you think i like playing?"))

response = model.invoke(messages)
print("RESPONSE", type(response), response, end="\n\n")
print("TOOL CALLS", type(response.tool_calls), response.tool_calls, end="\n\n")