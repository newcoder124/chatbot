## RAG ChatBot

Getting started
1. Set up the project environment

```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

2. Create an .env file. The .env file should be populated with the following environment variables:
```
OPENAI_API_KEY=<YOUR OPEN API KEY>

# LLM Models
AGENT_MODEL=<YOUR LLM model e.g. gpt-4o>

# Snowflake
SNOWFLAKE_USERNAME=<Your Snowflake user name>
SNOWFLAKE_PASSWORD=<Your Snowflake password>
SNOWFLAKE_ACCOUNT=<Your Snowflake account name>
SNOWFLAKE_DATABASE=<Your Snowflake schema name e.g. VERTICAL_CLASSIFICATION>
SNOWFLAKE_SCHEMA=<Your Snowflake schema name e.g. PUBLIC>
SNOWFLAKE_WAREHOUSE=<Your Snowflake warehouse name e.g. COMPUTE_WH>
SNOWFLAKE_ROLE=<Your Snowflake role e.g. ACCOUNTADMIN> 

# Vector DB
PINECONE_INDEX_NAME=<Your Pinecone index name e.g. test>
PINECONE_API_KEY=<YOUR Pinecone API Key>
```

3. Start the chatbot backend service (FastAPI)

```
fastapi dev chatbot_api/main.py
```

4. Start the frontend service (Streamlit)

```
streamlit run chatbot_frontend/src/main.py
```
