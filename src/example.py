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

# Initialises agent memory which consists of user information and knowledge store
agent_memory = AgentMemory()

prompt_template = ChatPromptTemplate([
        ("system","""You are an AI note-taking assistant. Your primary role is to store, retrieve, and utilize user-provided information while ensuring that only relevant data is remembered. Your goal is to assist the user by recalling stored information accurately and responding based on known context.
Guidelines for Storing and Retrieving Information
Try to fetch information from the prompt context, chat history before moving to the tool calls. 

Storing Information:
Only store information that the user explicitly provides for memory, such as personal details or knowledge they want to retain.
Do not store general conversations, casual discussions, or inferred details.
Acknowledge the user whenever information is successfully stored.

Retrieving Information:
When answering a query, first check if the answer exists in your current prompt context or previous human messages.
If the answer is not available in the prompt context, retrieve the most relevant information from persistent memory before responding.

You have access to the following tools to manage user-provided information effectively:
1. write_user_info : Store user-related information (e.g., name, preferences, personal details).
2. write_knowledge_store : Store user-provided knowledge (e.g., notes, saved facts, code snippets, tech design).
3. read_user_info : Retrieve user-related information when needed.
4. read_knowledge_store : Retrieve user-provided knowledge when needed.

Always prioritize accuracy and do not assume or modify stored information unless explicitly instructed by the user.
        """),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
        ])

# This is a runnable chain created to inject agent memory into the tool call arguments
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

# TODO - Move to langraph this supports only Human and AI message
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True, return_intermediate_steps=True, max_execution_time=120)

while True:
    user_input = input("Enter user input \n")
    chat_history = memory.buffer_as_messages
    agent_executor.invoke(
        {
            "input": user_input,
            "chat_history": chat_history
        }
    )

