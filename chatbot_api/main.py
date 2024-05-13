from fastapi import FastAPI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory import ChatMessageHistory

# from db import snowflake_db
from models.rag_query import QueryInput, QueryOutput
from agents.rag_agent import rag_agent_executor

chat_history_for_chain = ChatMessageHistory()

conversational_agent_executor = RunnableWithMessageHistory(
    rag_agent_executor,
    lambda session_id: chat_history_for_chain,
    input_messages_key="input",
    output_messages_key="output",
    history_messages_key="chat_history"
)

# User: Baxter-Auto, TapClicks

# Start FastAPI service
app = FastAPI(
    title="Marketing Chatbot",
    description="Endpoints for a chatbot assistant"
)

@app.get("/")
async def get_status():
    return {"status": "running"}

@app.post("/rag-agent")
async def ask_rag_agent(query: QueryInput) -> QueryOutput:
    # Invoke response
    response = conversational_agent_executor.invoke({
        "input": query.text
    }, {"configurable": {"session_id": "unused"}})
    
    response["intermediate_steps"] = [
        str(s) for s in response["intermediate_steps"]
    ]        
    # return response
    return {"input": response["input"], "output": response["output"], "intermediate_steps": response["intermediate_steps"]}