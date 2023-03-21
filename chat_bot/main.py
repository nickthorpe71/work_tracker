from langchain.agents import Tool
from langchain.memory import ConversationBufferMemory
from langchain import OpenAI
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.agents import initialize_agent

search = GoogleSearchAPIWrapper()
tools = [
    Tool(
        name = "Current Search",
        func=search.run,
        description="useful for when you need to answer questions about current events or the current state of the world"
    ),
]

memory = ConversationBufferMemory(memory_key="chat_history")

llm=OpenAI(temperature=0)
agent_chain = initialize_agent(tools, llm, agent="conversational-react-description", verbose=True, memory=memory)

agent_chain.run(input="tell me my name in english then in spanish then in cantonese")