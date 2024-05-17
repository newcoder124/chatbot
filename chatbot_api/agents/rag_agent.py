import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_openai_functions_agent, Tool, AgentExecutor
from langchain_openai import ChatOpenAI
from chains.snowflake_sql_chain import sql_agent
from chains.vectorstore_chain import set_retriever
from tools.ltv_calculator import get_advertiser_ltv_value

# Load environment variables from .env file
load_dotenv()

# Set agent chat model
AGENT_MODEL=os.getenv("AGENT_MODEL")

# Define system prompts for different modes
system_prompts = {
    "default": """You are a data-driven marketing expert who provides insights and recommendations with numbers.
Your task is to answer the user's question with the help of tools, if needed. You have access to a vectorstore which
contains relevant information about advertiser, industry-level and ad platform data. You also have access to snowflakes which you can
query to retrieve any specific datapoints that are required to answer the user's question. I encourage you to use the vectorstore
first. And, if you do not find meaningful information to answer the question, then use snowflakes. If you do not know the answer,
then just say that you do not know.

Considerations:
1. Do not answer questions that are not related to marketing. Re-direct the user to ask marketing-related questions by providing some suggestions.
2. Provide commentaries with numbers.
3. You do not need to use tools unless you need it.
4. Be factual. Do not make up any numbers. 
5. Bonus point if you sound like an analyst from McKinsey.
6. Make the response no more than 300 words at most.

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

---""",
    "Baxter-Auto": """I am a marketing agent for Baxter-Auto...""",
    "TapClicks": """I am a marketing agent for TapClicks..."""
}

def create_rag_agent(mode):
    system_prompt_str = system_prompts.get(mode, system_prompts["default"])

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt_str),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    tools = [
        Tool(
            name="SnowflakeSQL",
            func=sql_agent.invoke,
            description="""Use this to query advertiser data that you could not retrieve from
vectorstore. For instance, you can use this to retrieve specific data about a particular
campaign that the advertiser ran."""
        ),
        Tool(
            name="VectorStore",
            func=set_retriever(mode).invoke,
            description="""Use this when you need to retrieve contexts about advertiser
and industry level data. The vectorstore contains the snapshots of the latest trends
including impression, clicks, spend, click-through-rate (CTR) and cost-per-click (CPC). This
will help you answer questions such as 'How's the marketing performance the past couple months?',
'How's the automotive industry doing?', 'What other ad platform do you recommend I use?'"""
        )
    ]

    chat_model = ChatOpenAI(
        model=AGENT_MODEL,
        temperature=0
    )

    rag_agent = create_openai_functions_agent(
        llm=chat_model,
        prompt=prompt,
        tools=tools
    )

    return AgentExecutor(
        agent=rag_agent,
        tools=tools,
        return_intermediate_steps=True,
        verbose=True
    )