from langchain.globals import set_debug, set_verbose
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import chain
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.agents.output_parsers.tools import ToolAgentAction
from langchain.memory import ConversationBufferMemory

from llm.gemini import gemini
from tools import tools
from memory.agent_memory import AgentMemory

set_debug(True)
set_verbose(True)

agent_memory = AgentMemory()

# Agent Executor

prompt_template = ChatPromptTemplate([
        ("system","""You are a chatbot.
            You have the following tasks to perform:
                1. If the user gives any information about them or asks you to remember some text, you have to store it in your persistent memory. Acknowledge the user that you have stored the information in memory.
                2. If the user asks a query/question, you should check if the human has provided the answer before in your prompt context first.
                3. If the user asks a query/question and the answer is not available in the prompt context, retrieve the most relevant information from your persistent memory.
            You have the following available tools to perform the above tasks:
                1. write_user_info - Tool to store any user related information into persistent memory
                2. write_knowledge_store - Tool to store any user provided knowledge into persistent memory
                3. read_knowledge_store - Tool to retrieve any user provided knowledge from persistent memory
                4. read_user_info - Tool to retrieve user related information from persistent memory
        """),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
        ])

# prompt = prompt_template.invoke({"chat_history":[]})

@chain
def inject_agent_memory(tool_agent_actions):
    print("TOOL AGENT ACTIONS", tool_agent_actions, end="\n\n\n")
    print("TYPE TOOL AGENT ACTIONS", type(tool_agent_actions), end="\n\n\n")

    if isinstance(tool_agent_actions, list):

        for action in tool_agent_actions:
            if isinstance(action, ToolAgentAction):
                action.tool_input["agent_memory"] = agent_memory
    
    return tool_agent_actions


agent = create_tool_calling_agent(llm=gemini, tools=tools, prompt=prompt_template) | inject_agent_memory
# print("PROMPT TEMPLATE", agent.steps[1].messages, end="\n\n\n")

# TODO - Move to langraph this supports only Human and AI message
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True)

while True:
    user_input = input("Enter user input \n")
    chat_history = memory.buffer_as_messages
    agent_executor.invoke(
        {
            "input": user_input,
            "chat_history": chat_history
        }
    )

