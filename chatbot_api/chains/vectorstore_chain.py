import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder,    
)

# Load environment variables from .env file
load_dotenv()

# Set environment parameters
AGENT_MODEL = os.getenv("AGENT_MODEL")
pinecone_api_key = os.getenv('PINECONE_API_KEY')
index_name = os.getenv('PINECONE_INDEX_NAME')
embedding = OpenAIEmbeddings()

### Ingest code - you may need to run this the first time

# Instantiate vector store object
vectorstore = PineconeVectorStore.from_existing_index(
    index_name, embedding
)

# Create a retriever
def set_retriever(mode):
    filter = None
    if mode == "Baxter-Auto":
        filter={"$or": [
            {"vertical": 'Automotive'},
            {"advertiser": mode}
        ]}

    return vectorstore.as_retriever(
        search_type='similarity', 
        search_kwargs={
            'k': 5,
            'filter': filter
        }
    )