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
# # Load
# from langchain_community.document_loaders import WebBaseLoader
# loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")
# data = loader.load()

# # Split
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
# all_splits = text_splitter.split_documents(data)

# # Add to vectorDB
# vectorstore = PineconeVectorStore.from_documents(
#     documents=all_splits, embedding=OpenAIEmbeddings(), index_name=PINECONE_INDEX_NAME
# )
# retriever = vectorstore.as_retriever()

# Instantiate vector store object
vectorstore = PineconeVectorStore.from_existing_index(
    index_name, embedding
)

# Create a retriever
retriever = vectorstore.as_retriever(
    search_type='similarity', 
    search_kwargs={'k': 3}
)

# # Create prompt
# prompt_template = """Your job is to use descriptions about
# advertiser data to answer questions that help advertisers
# improve marketing performance. Be as detailed as possible, and
# do not make up any information not from the context. If you
# do not know the answer, say that you do not know.

# Context: {context}
# """

# custom_prompt = PromptTemplate(
#     template=prompt_template,
#     input_variables=["context"]
# )

# system_prompt = SystemMessagePromptTemplate(prompt=custom_prompt)
# human_prompt = HumanMessagePromptTemplate(
#     prompt=PromptTemplate(input_variables=["input"], template="{input}")
# )

# messages = [system_prompt, human_prompt]

# chat_prompt = ChatPromptTemplate(
#     input_variables=["context", "input"], messages=messages
# )

# # chat_prompt = ChatPromptTemplate.from_messages(
# #     [
# #         SystemMessagePromptTemplate(prompt=custom_prompt),
# #         ("human", "{input}"),
# #         MessagesPlaceholder("agent_scratchpad"),
# #     ]
# # )

# # Create chain
# vectorstore_chain = RetrievalQA.from_chain_type(
#     llm=ChatOpenAI(model=AGENT_MODEL, temperature=0),
#     retriever=retriever
# )
# vectorstore_chain.combine_documents_chain.llm_chain.prompt = chat_prompt

# print(vectorstore_chain.invoke({"input": "Give me ad campaign"}))



# # Test namespace
# # vectorstore.add_texts(["i worked at kensho"], namespace="harrison")
# # vectorstore.add_texts(["i worked at facebook"], namespace="ankush")
# from langchain_core.runnables import ConfigurableField

# configurable_retriever = retriever.configurable_fields(
#     search_kwargs=ConfigurableField(
#         id="search_kwargs",
#         name="Search Kwargs",
#         description="The search kwargs to use",
#     )
# )

# print(configurable_retriever.invoke(
#     "where did the user work?",
#     config={"configurable": {"search_kwargs": {"namespace": "harrison"}}},
# ))