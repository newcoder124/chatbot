import json

# content = """{"commentary": "Baxter Auto, an automotive company, has shown varied marketing performance over the past 12 months. Here's a detailed analysis:

# 1. **Overall Performance**:
#    - **Total Impressions**: 9,116
#    - **Total Clicks**: 850
#    - **Total Spend**: $1,150.28
#    - **CTR (Click-Through Rate)**: 9.3%
#    - **CPC (Cost Per Click)**: $1.35
#    - **Number of Campaigns**: 11

# 2. **Monthly Performance**:
#    - The impressions ranged from a low of 57 in April 2024 to a high of 1,929 in September 2023.
#    - Clicks varied from 21 in January 2024 to 194 in September 2023.
#    - Spend ranged from $8.38 in April 2024 to $293.52 in September 2023.
#    - CTR fluctuated, with the highest being 19.4% in April 2024 and the lowest at 5.6% in March 2024.
#    - CPC was lowest at $0.405 in March 2024 and highest at $1.171 in November 2023.

# 3. **Trends**:
#    - There was a significant drop in impressions and clicks in April 2024 compared to previous months.
#    - The spend also saw a decline in April 2024, indicating a possible reduction in campaign activity or budget.
#    - Despite lower impressions in April 2024, the CTR was notably high at 19.4%, suggesting effective targeting.

# 4. **Month-over-Month (MoM) Performance**:
#    - April 2024 saw a 98% decrease in impressions and an 89.5% decrease in clicks compared to March 2024.
#    - Spend decreased by 83% in April 2024 compared to March 2024.
#    - CTR increased by 4.16% in April 2024, indicating improved engagement despite lower reach.

# In summary, Baxter Auto's marketing performance has been inconsistent, with significant fluctuations in key metrics. The high CTR in April 2024 suggests effective targeting, but the overall decline in impressions and spend indicates a need for strategic adjustments to maintain consistent performance.", "plot": "line_chart", "index": "MONTH_YR", "chart_data": {"MONTH_YR": ["2024-04-01", "2024-03-01", "2024-02-01", "2024-01-01", "2023-12-01", "2023-11-01", "2023-10-01", "2023-09-01", "2023-08-01", "2023-07-01", "2023-06-01", "2023-05-01"], "TOTAL_IMPRESSIONS": [57, 1324, 792, 192, 273, 387, 1017, 1929, 526, 1110, 1068, 441], "TOTAL_CLICKS": [22, 132, 91, 21, 27, 35, 60, 194, 51, 90, 100, 27], "TOTAL_SPEND": [8.38, 135.27, 97.69, 23.58, 39.65, 77.76, 114.39, 293.52, 73.76, 119.99, 130.24, 36.05], "AVERAGE_CTR": [0.194, 0.056, 0.085, 0.145, 0.099, 0.101, 0.062, 0.085, 0.088, 0.086, 0.079, 0.057], "AVERAGE_CPC": [0.479, 0.405, 0.415, 0.441, 0.775, 1.171, 0.814, 0.843, 0.504, 0.41, 0.499, 0.44]}}"""

# content = '''{
#     "commentary": "Baxter Auto, an automotive company, has shown varied marketing performance over the past 12 months. Here's a detailed analysis:\\n\\n1. **Overall Performance**:\\n   - **Total Impressions**: 9,116\\n   - **Total Clicks**: 850\\n   - **Total Spend**: $1,150.28\\n   - **CTR (Click-Through Rate)**: 9.3%\\n   - **CPC (Cost Per Click)**: $1.35\\n   - **Number of Campaigns**: 11\\n\\n2. **Monthly Performance**:\\n   - The impressions ranged from a low of 57 in April 2024 to a high of 1,929 in September 2023.\\n   - Clicks varied from 21 in January 2024 to 194 in September 2023.\\n   - Spend ranged from $8.38 in April 2024 to $293.52 in September 2023.\\n   - CTR fluctuated, with the highest being 19.4% in April 2024 and the lowest at 5.6% in March 2024.\\n   - CPC was lowest at $0.405 in March 2024 and highest at $1.171 in November 2023.\\n\\n3. **Trends**:\\n   - There was a significant drop in impressions and clicks in April 2024 compared to previous months.\\n   - The spend also saw a decline in April 2024, indicating a possible reduction in campaign activity or budget.\\n   - Despite lower impressions in April 2024, the CTR was notably high at 19.4%, suggesting effective targeting.\\n\\n4. **Month-over-Month (MoM) Performance**:\\n   - April 2024 saw a 98% decrease in impressions and an 89.5% decrease in clicks compared to March 2024.\\n   - Spend decreased by 83% in April 2024 compared to March 2024.\\n   - CTR increased by 4.16% in April 2024, indicating improved engagement despite lower reach.\\n\\nIn summary, Baxter Auto's marketing performance has been inconsistent, with significant fluctuations in key metrics. The high CTR in April 2024 suggests effective targeting, but the overall decline in impressions and spend indicates a need for strategic adjustments to maintain consistent performance.",
#     "plot": "line_chart",
#     "index": "MONTH_YR",
#     "chart_data": {
#         "MONTH_YR": ["2024-04-01", "2024-03-01", "2024-02-01", "2024-01-01", "2023-12-01", "2023-11-01", "2023-10-01", "2023-09-01", "2023-08-01", "2023-07-01", "2023-06-01", "2023-05-01"],
#         "TOTAL_IMPRESSIONS": [57, 1324, 792, 192, 273, 387, 1017, 1929, 526, 1110, 1068, 441],
#         "TOTAL_CLICKS": [22, 132, 91, 21, 27, 35, 60, 194, 51, 90, 100, 27],
#         "TOTAL_SPEND": [8.38, 135.27, 97.69, 23.58, 39.65, 77.76, 114.39, 293.52, 73.76, 119.99, 130.24, 36.05],
#         "AVERAGE_CTR": [0.194, 0.056, 0.085, 0.145, 0.099, 0.101, 0.062, 0.085, 0.088, 0.086, 0.079, 0.057],
#         "AVERAGE_CPC": [0.479, 0.405, 0.415, 0.441, 0.775, 1.171, 0.814, 0.843, 0.504, 0.41, 0.499, 0.44]
#     }
# }'''

# content = '''{"commentary": "Baxter Auto, an automotive company, has shown varied marketing performance over the past 12 months from April 2023 to April 2024. Here's a detailed analysis: Overall, Baxter Auto's marketing performance has been inconsistent, with notable peaks and troughs in key metrics. The high CTR in April 2024 suggests effective targeting, but the low impressions and clicks indicate a need for broader reach. The fluctuating CPC also suggests varying cost efficiency across campaigns. To improve, Baxter Auto should focus on stabilizing their impressions and clicks while maintaining or improving their CTR and CPC.",
#     "plot": "line_chart",
#     "index": "MONTH_YR",
#     "chart_data": {
#         "MONTH_YR": ["2024-04-01", "2024-03-01", "2024-02-01", "2024-01-01", "2023-12-01", "2023-11-01", "2023-10-01", "2023-09-01", "2023-08-01", "2023-07-01", "2023-06-01", "2023-05-01"],
#         "TOTAL_IMPRESSIONS": [57, 1324, 792, 192, 273, 387, 1017, 1929, 526, 1110, 1068, 441],
#         "TOTAL_CLICKS": [22, 132, 91, 21, 27, 35, 60, 194, 51, 90, 100, 27],
#         "TOTAL_SPEND": [8.38, 135.27, 97.69, 23.58, 39.65, 77.76, 114.39, 293.52, 73.76, 119.99, 130.24, 36.05],
#         "AVERAGE_CTR": [0.194, 0.056, 0.085, 0.145, 0.099, 0.101, 0.062, 0.085, 0.088, 0.086, 0.079, 0.057],
#         "AVERAGE_CPC": [0.479, 0.405, 0.415, 0.441, 0.775, 1.171, 0.814, 0.843, 0.504, 0.41, 0.499, 0.44]
#     }
# }'''

def parse_message_content(content):
    try:
        print('Returning this!')
        return json.loads(content)
    except json.JSONDecodeError:
        print('But it errored!')
        return {"commentary": content}

# print(parse_message_content(content))