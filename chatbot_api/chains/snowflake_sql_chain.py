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
# tables_to_include = ['advertiser_monthly_data', 'vertical_benchmark_data', 'global_benchmark_data', 'analysis_data']
tables_to_include = ['vertical_benchmark_data','analysis_data']
snowflake_db = SQLDatabase.from_uri(snowflake_url, sample_rows_in_table_info=10, include_tables=tables_to_include)
#  for the advertiser {advertiser}

# # Prompt
# custom_prompt = PromptTemplate(
#     template="""You are an SQL expert answers marketing questions. I want you to following the
# following steps:

# 1. Generate SQL query: Answer the user's question by providing a SQL query that can be run against the Snowflake database. If
# the query uses llm_automotive_advertiser_data table, filter the account_descriptive_name on the advertiser, {advertiser}. Unless
# the user specifies in his question a specific number of examples he wishes to obtain, always limit your query to at most {top_k} results.

# 2. Interpret the result: Answer the user's question by interpreting the SQL query result. Make sure you provide a commentary with numbers from the SQL result.

# Remember:
# 1. Provide a commentary with actual numbers from the SQL result.
# 2. Be mindful of the database schema.
# 3. If the question is about marketing performance, make sure to include CTC and CTR in your query generation.
# 4. Make sure that your response is no more than 250 words.

# ---

# Only use the following tables:
# {table_info}

# Additional notes about the tables:
# * llm_automotive_advertiser_data contains the monthly level individual campaign performance data
# * llm_vertical_classification_table contains the industry benchmark data
# * Note that CTC is cost-per-click and CTR is click-through rate

# ---

# Here's an example answer:

# It appears that the advertiser campaign for an automotive product experienced a significant increase in impressions and clicks from September 2023 onwards.

# -September 2023: There was a substantial jump in impressions (2905) compared to previous months (highest being 104 in August 2023). Clicks also rose significantly (465) in September compared to all prior months (highest was 6 in June 2023).
# -October - December 2023: Impressions remained considerably high (above 180) throughout this period, with clicks also staying above 20.
# -January - March 2024: There appears to be a leveling off in both impressions (around 200) and clicks (around 25).

# This pattern suggests a possible strategic shift in the campaign around September 2023. Here are some possible explanations:

# -New campaign launch: A new marketing campaign launched in September 2023 could explain the rise in impressions and clicks. This could have involved new advertising placements, a different creative approach, or a targeted social media push.
# -Seasonal influence: There could be a seasonal factor at play, with car promotions typically increasing around fall/winter months to target holiday sales.
# -Change in targeting: The advertiser may have refined their target audience in September, resulting in a higher number of relevant impressions and clicks.

# Here's another example answer:

# In 2022, Baxter Auto's marketing performance showed a distinct pattern when compared to industry benchmarks for the automotive sector. Here's a detailed comparison:

# 1. Impressions and Clicks:
#    - Baxter Auto had significantly fewer impressions and clicks throughout the year compared to industry benchmarks. For instance, in January, Baxter Auto had 1,415 impressions and 70 clicks, whereas the industry had 1,326,640,897 impressions and 18,217,343 clicks.

# 2. Click-Through Rate (CTR):
#    - Baxter Auto generally had a higher CTR compared to the industry average. For example, in September, Baxter Auto's CTR was 0.1057, significantly higher than the industry's 0.0501.

# 3. Cost-Per-Click (CPC):
#    - Baxter Auto's CPC was consistently lower than the industry average. In December, Baxter Auto's CPC was $0.585, while the industry's was $2.250.

# Overall, while Baxter Auto had much lower visibility in terms of impressions and clicks, their campaigns were more efficient, achieving higher engagement (CTR) and at a lower cost per engagement (CPC) compared to the broader industry benchmarks. This suggests that Baxter Auto's campaigns were highly targeted and effective at engaging a smaller, perhaps more relevant audience.

# ---

# Question: {input}
# Your Answer:
# """,
#     input_variables=["input", "top_k", "table_info"],
#     partial_variables={"advertiser": "Baxter Auto"}
# )

# Prompt
# custom_prompt = PromptTemplate(
#     template="""You are an SQL expert answers marketing questions. I want you to following the
# following steps:

# 1. Generate SQL query: Answer the user's question by providing a SQL query that can be run against the Snowflake database. Unless
# the user specifies in his question a specific number of examples he wishes to obtain, always limit your query to at most {top_k} results.

# 2. Format the SQL output: Render the values in a table in a nice format. Then, provide your interpretation. Make sure you only provide the fields you will use
# in your interpretation.

# 3. Interpret the result: Answer the user's question by interpreting the SQL query result. Make sure you provide a commentary with numbers from the SQL result.

# 4. Look out for keywords like "How does it compare against X". If the question involves comparing an advertiser's CTR, CTC, and Spend against its vertical or global,
# avoid using CTR, CTC, Spend columns at the vertical/global level or calculating from scratch. Rather, use the existing columns with the "_average_" stem as it contains the monthly averages across
# advertisers which you want to compare against. Also consider using columns with "comparison_" prefix as it contains the relative difference (in %) between the advertiser.

# Remember:
# 1. Provide a commentary with actual numbers from the SQL result.
# 2. Be mindful of the database schema.
# 3. If the question is about marketing performance, make sure to include CTC and CTR in your query generation.
# 4. Make sure that your response is no more than 250 words.
# 5. CTR is in fraction form, represent it in percentage form.

# ---

# Only use the following tables:
# {table_info}

# Additional notes about the tables:
# - CTR is click-through-rate, which is click / impression
# - CTC is cost-per-click, which is spend / click
# - Any columns with prefixes that start with 'comparison_' is relative difference. For instance
# comparison_ctr_adv_vs_vert is the relative difference of CTR between advertiser and its corresponding vertical
# - Use vertical_benchmark_data on questions pertaining to vertical level.
# - Use global_benchmark_data on questions pertaining to global level.
# ---

# ---

# Question: {input}
# Your Answer:
# """,
#     input_variables=["input", "top_k", "table_info"],
#     partial_variables={"advertiser": "Baxter Auto"}
# )

# Instruction
# Expected Output
# - Format tips
# Instruction on how to filter on date range, and when to roll it up at the advertiser level

custom_prompt = PromptTemplate(
    template="""You are an SQL expert that retrieves relevant data to address the user's question.
Answer the user's question by providing an SQL query that is executable in the Snowflake database. 
Then, output that table in a clean format. Unless the user specifies in his question a number of 
examples he wishes to obtain, always limit your query to at most {top_k} results. If the
question is general, as in, "What's my marketing performance?," filter for the past 12 months.

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