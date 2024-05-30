import os
from dotenv import load_dotenv
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain_openai import ChatOpenAI
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent

# Load environment variables from .env file
load_dotenv()

# Set agent chat model
AGENT_MODEL=os.getenv("AGENT_MODEL")

# snowflake connection
username = os.getenv('SNOWFLAKE_USERNAME')
password = os.getenv('SNOWFLAKE_PASSWORD')
snowflake_account = os.getenv('SNOWFLAKE_ACCOUNT')
database = os.getenv('SNOWFLAKE_DATABASE')
schema = os.getenv('SNOWFLAKE_SCHEMA')
warehouse = os.getenv('SNOWFLAKE_WAREHOUSE')
role = os.getenv('SNOWFLAKE_ROLE')
snowflake_url = f"snowflake://{username}:{password}@{snowflake_account}/{database}/{schema}?warehouse={warehouse}&role={role}"

# Connect to Snowflakes database
tables_to_include = ['vertical_benchmark_data','analysis_data']
snowflake_db = SQLDatabase.from_uri(snowflake_url, sample_rows_in_table_info=10, include_tables=tables_to_include)

custom_prompt = PromptTemplate(
    template="""You are an SQL expert that retrieves relevant data to address the user's question.
Answer the user's question by providing an SQL query that is executable in the Snowflake database. 
Then, output that table in a clean format. Unless the user specifies in his question a number of 
examples he wishes to obtain, always limit your query to at most {top_k} results. If the
question is general, as in, "What's my marketing performance?," filter for the past 12 months.

*If the query does not return any result, do not return any made-up tables! Just return no values.

If the question requires implies making a comparison between an advertiser(s) and its vertical, which means
the industry that the advertiser belongs to, use the analysis_data table. Here are additional details about
how to handle comparison questions:

Question Examples:
- How does an advertiser(s) compare against peers in the vertical benchmark?
- How does an advertiser(s) compare against its vertical benchmark?
- How is the spending of advertiser(s) against its peers?

Table to Use: analysis_data

Metrics to Select for Comparison (unless specified): 

1. Clicks-through-rate (CTR): advertiser_ctr, vertical_average_ctr, comparison_ctr_adv_vs_vert
2. Cost-per-click (CPC): advertiser_cpc, vertical_cpc, comparison_cpc_adv_vs_vert
3. Spend: advertiser_spend, vertical_average_spend, comparison_spend_adv_vs_vert

Example Query:

SELECT 
    month_yr, 
    account_descriptive_name, 
    advertiser_ctr, 
    vertical_ctr, 
    comparison_ctr_adv_vs_vert,
    advertiser_cpc, 
    vertical_cpc, 
    comparison_cpc_adv_vs_vert,
    advertiser_spend, 
    vertical_average_spend, 
    comparison_spend_adv_vs_vert
FROM analysis_data
WHERE account_descriptive_name = 'Baxter Auto'
    AND predicted_vertical_1 = 'Automotive'
AND month_yr >= DATEADD(MONTH, -12, CURRENT_DATE)
ORDER BY MONTH_YR DESC; 

Table Output Instruction:
- Provide a sentence on the date range of the table output
- Format it in a clean way.

---

Only use the following tables:
{table_info}

---

Question: {input}
Your Table Output:
""",
    input_variables=["input", "top_k", "table_info"],
    partial_variables={"advertiser": "Baxter Auto"}
)

full_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate(prompt=custom_prompt),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)

# Instantiate chat model
chat_model = ChatOpenAI(
    model=AGENT_MODEL,
    temperature=0
)

sql_agent = create_sql_agent(
    llm=chat_model,
    db=snowflake_db,    
    prompt=full_prompt,
    top_k=24,
    verbose=True,
    agent_type="openai-tools",
)