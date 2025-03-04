import os
import snowflake
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory import ChatMessageHistory
import asyncio
import json

# from db import snowflake_db
from models.rag_query import QueryInput, QueryOutput
from agents.rag_agent import create_rag_agent

# SQL Connection
# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# snowflake connection
conn = snowflake.connector.connect(
    user=os.getenv('SNOWFLAKE_USERNAME'),
    password=os.getenv('SNOWFLAKE_PASSWORD'),
    account=os.getenv('SNOWFLAKE_ACCOUNT'),
    warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
    database=os.getenv('SNOWFLAKE_DATABASE'),
    schema=os.getenv('SNOWFLAKE_SCHEMA')
)

# Create a cursor object
cur = conn.cursor()

# Chat history
chat_history_for_chain = ChatMessageHistory()

# Start FastAPI service
app = FastAPI(
    title="Marketing Chatbot",
    description="Endpoints for a chatbot assistant"
)

# Dictionary to store user modes
user_modes = {}

class ModeRequest(BaseModel):
    session_id: str
    mode: str

class RagAgentRequest(BaseModel):
    text: str
    session_id: str
    mode: str

app = FastAPI(
    title="Marketing Chatbot",
    description="Endpoints for a chatbot assistant"
)

# Endpoints
@app.get("/")
async def get_status():
    return {"status": "running"}

@app.post("/set-mode")
async def set_mode(mode_request: ModeRequest):
    user_modes[mode_request.session_id] = mode_request.mode
    
    # Set SQL policy
    sql_response = None
    if mode_request.mode == "juno":                
        try:
            cur.execute("ALTER TABLE analysis_data ADD ROW ACCESS POLICY agency_row_access_policy ON (subdomain);")  
        except:
            pass 
    else:
        try:
            cur.execute("ALTER TABLE analysis_data DROP ROW ACCESS POLICY agency_row_access_policy;")  
        except:
            pass         
    
    return {"status": "mode set", "session_id": mode_request.session_id, "mode": mode_request.mode}

def get_agent_executor(mode: str):
    # Create a RAG agent with the specified mode
    agent_executor = create_rag_agent(mode)

    # Create a conversational agent executor
    conversational_agent_executor = RunnableWithMessageHistory(
        agent_executor,
        lambda session_id: chat_history_for_chain,
        input_messages_key="input",
        output_messages_key="output",
        history_messages_key="chat_history"
    )

    return conversational_agent_executor

def get_executor(request: RagAgentRequest):
    mode = user_modes.get(request.session_id, "default")
    return get_agent_executor(mode)

@app.post("/rag-agent")
async def ask_rag_agent(request: RagAgentRequest, executor=Depends(get_executor)) -> QueryOutput:
    async def text_streamer():
        response = executor.invoke({
            "input": request.text,
        }, {"configurable": {"session_id": request.session_id}})
        
        # Send intermediate steps
        for step in response["intermediate_steps"]:
            yield json.dumps({"type": "step", "content": str(step)}) + "\n"
            await asyncio.sleep(0.1)  # Simulate delay for streaming
        
        # Send the final output
        output = response['output']
        yield json.dumps({"type": "output", "content": output})

    return StreamingResponse(text_streamer(), media_type="application/json")