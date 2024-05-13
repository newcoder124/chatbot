# Load environment libraries
from dotenv import load_dotenv

# Load langchain libraries
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate
)    
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()

# Create chat prompt template
system_prompt_template_str = """You are a helpful chatbot who's an expert in marketing.
Only answer questiones related to marketing.
"""

# Create a system message prompt template
system_prompt = SystemMessagePromptTemplate(
    prompt=PromptTemplate(
        template=system_prompt_template_str,
        input_variables=[],
    )
)

# Create a human message prompt template
human_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(
        template="{question}",
        input_variables=["question"],
    )
)

messages = [system_prompt, human_prompt]
prompt_template = ChatPromptTemplate(
    input_variables=["question"],
    messages=messages
)

# Create a chat prompt template
chat_model = ChatOpenAI(
    model="gpt-3.5-turbo-0125", 
    temperature=0)
chain = prompt_template | chat_model | StrOutputParser()
chain.invoke({"question": "How should I optimize my campaign spend?"})
print(chain.invoke({"question": "Repeat what I asked before."}))