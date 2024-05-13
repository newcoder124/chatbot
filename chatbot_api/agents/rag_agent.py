import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_openai_functions_agent, Tool, AgentExecutor
from langchain_openai import ChatOpenAI
from chains.snowflake_sql_chain import sql_agent
from chains.vectorstore_chain import retriever
from tools.ltv_calculator import get_advertiser_ltv_value

# Load environment variables from .env file
load_dotenv()

# Set agent chat model
AGENT_MODEL=os.getenv("AGENT_MODEL")

# Set agent prompt
system_prompt_str = """You are a marketing expert who provides insights and recommendations that are 
data-driven. Your task is to answer a user's question and use a tool to gather information, if needed. 

Considerations:
1. Do not answer questions that are not related to marketing.
2. Provide commentaries with numbers.
3. You do not need to use tools for every query.
4. Be specific and factual. If you have contexts from RAG, use that information to provide insights and recommendations.

---

Here's an example response:

In 2022, Baxter Auto's marketing performance showed a distinct pattern when compared to industry benchmarks for the automotive sector. Here's a detailed comparison:

1. Impressions and Clicks:
   - Baxter Auto had significantly fewer impressions and clicks throughout the year compared to industry benchmarks. For instance, in January, Baxter Auto had 1,415 impressions and 70 clicks, whereas the industry had 1,326,640,897 impressions and 18,217,343 clicks.

2. Click-Through Rate (CTR):
   - Baxter Auto generally had a higher CTR compared to the industry average. For example, in September, Baxter Auto's CTR was 0.1057, significantly higher than the industry's 0.0501.

3. Cost-Per-Click (CPC):
   - Baxter Auto's CPC was consistently lower than the industry average. In December, Baxter Auto's CPC was $0.585, while the industry's was $2.250.

Overall, while Baxter Auto had much lower visibility in terms of impressions and clicks, their campaigns were more efficient, achieving higher engagement (CTR) and at a lower cost per engagement (CPC) compared to the broader industry benchmarks. This suggests that Baxter Auto's campaigns were highly targeted and effective at engaging a smaller, perhaps more relevant audience.

---

"""

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            system_prompt_str
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# Set agent tools
tools = [
    Tool(
        name="LifetimeValueCalculator",
        func=get_advertiser_ltv_value,
        description="""Use this function to calculate the lifetime value at 
        the advertiser level."""
    ),
    Tool(
        name="SnowflakeSQL",        
        func=sql_agent.invoke,
        description="""Use this to query advertiser data. This will help 
        you answer questions about marketing trends and performance."""
    ),
    Tool(
        name="VectorStore",
        func=retriever.invoke,
        description="""Use this when you need to provide Ad campaign recommendations.
For instance, the question may include, 'Should I consider using another ad campaign?'    
"""
    )
]

# Instantiate chat model
chat_model = ChatOpenAI(
    model=AGENT_MODEL,
    temperature=0
)

# Instantiate a rag agent
rag_agent = create_openai_functions_agent(
    llm=chat_model,
    prompt=prompt,
    tools=tools
)

# Create an agent executor
rag_agent_executor = AgentExecutor(
    agent=rag_agent,
    tools=tools,
    return_intermediate_steps=True,
    verbose=True
)