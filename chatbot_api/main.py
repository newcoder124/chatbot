from fastapi import FastAPI, Depends
from pydantic import BaseModel
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory import ChatMessageHistory

# from db import snowflake_db
from models.rag_query import QueryInput, QueryOutput
from agents.rag_agent import create_rag_agent
# from agents.rag_agent import rag_agent_executor

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

    response = executor.invoke({
        "input": request.text,
    }, {"configurable": {"session_id": request.session_id}})
    
    response["intermediate_steps"] = [
        str(s) for s in response["intermediate_steps"]
    ]
    return {"input": response["input"], "output": response["output"], "intermediate_steps": response["intermediate_steps"]}
