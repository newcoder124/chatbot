import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()

AGENT_MODEL = os.getenv("AGENT_MODEL")
API_KEY = os.getenv('PINECONE_API_KEY')
INDEX_NAME = 'test' #os.getenv('PINECONE_INDEX_NAME')
EMBEDDING = OpenAIEmbeddings()

# Instantiate an existing pinecone index
vectorstore = PineconeVectorStore.from_existing_index(
    index_name=INDEX_NAME, embedding=EMBEDDING
)

# Ingest documents 
# vectorstore.add_texts(["Advertiser A Data: Mean=24"], metadatas=[{"advertiser": "A", "agency": "A"}])
# vectorstore.add_texts(["Advertiser A Data: STD=24"], metadatas=[{"advertiser": "A", "agency": "A"}])
# vectorstore.add_texts(["Advertiser B Data: Mean=50"], metadatas=[{"advertiser": "B", "agency": "A"}])
# vectorstore.add_texts(["Advertiser B Data: STD=12"], metadatas=[{"advertiser": "B", "agency": "A"}])
# vectorstore.add_texts(["Advertiser C Data: Mean=55"], metadatas=[{"advertiser": "C", "agency": "C"}])
# vectorstore.add_texts(["Advertiser C Data: STD=25"], metadatas=[{"advertiser": "C", "agency": "C"}])
# vectorstore.add_texts(["Automotive Trend: Mean=25"], metadatas=[{"vertical": "automotive"}])
# vectorstore.add_texts(["Global marketing stats: Mean=555"])

# Mode
query = "STD"
mode = "Advertiser" # Agency, Global
entity_name = "D"
entity_vertical = "automotive"

# retriever = None
filter = None
if mode == "Advertiser":
    filter={"$or": [
        {"vertical": entity_vertical},
        {"advertiser": entity_name}
    ]}
elif mode == "Agency":
    filter={"agency": entity_name}

results = vectorstore.similarity_search(
    query,
    filter=filter
)

for result in results:
    print(result.page_content)