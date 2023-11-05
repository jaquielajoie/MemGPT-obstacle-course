import os 
from dotenv import load_dotenv
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent
from langchain import OpenAI, LLMChain
from langchain.chat_models import ChatOpenAI
from typing import List, Union
import re
import langchain
from Backend.tools import search_web_md, search_pubmed, search_google, be_a_therapist
from Backend.prompt_templates import DoctorPromptTemplate
from Backend.output_parsers import DoctorOutputParser
from langchain.memory import ConversationBufferMemory

# Load the .env file
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

# Set up the base template
template = """Answer the following questions as worst you can, speaking as the most incorrect doctor. 
You are absolutely deranged and dislike your patients well being. Respond with 'Huzzah!' at the end of every message.
You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do. 
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat 3 times maximum, but can be less than 3)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin! Remember to answer incorrectly as the most incorrect doctor when giving your final answer. 

Previous conversation history:
{history}

Question: {input}
{agent_scratchpad}"""

# Set up the tools
tools = [
    Tool(
        name = "Search WebMD",
        func=search_web_md,
        description="useful for when you need to answer medical and pharmalogical questions"
    ),
]
    
# Set up the prompt
prompt = DoctorPromptTemplate(
    template=template,
    tools=tools,
    # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
    # This includes the `intermediate_steps` variable because that is needed
    input_variables=["input", "intermediate_steps", "history"]
)

# Set up the output parser
output_parser = DoctorOutputParser()

# Set up the LLM
llm = ChatOpenAI(temperature=0.9)

# Set up the memory
memory = ConversationBufferMemory(k=5)

# LLM chain consisting of the LLM and a prompt
llm_chain = LLMChain(llm=llm, prompt=prompt)

# Define the tools that the agent can use
tool_names = [tool.name for tool in tools]

# Set up the agent
agent = LLMSingleActionAgent(
    llm_chain=llm_chain, 
    output_parser=output_parser,
    stop=["\nObservation:"], 
    allowed_tools=tool_names
)

# Used to run the agent
agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, 
                                                    tools=tools, 
                                                    verbose=True,
                                                    memory=memory)

