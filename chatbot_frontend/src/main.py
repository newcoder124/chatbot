import os
import json
import requests
import numpy as np
import pandas as pd
import streamlit as st
from utility import parse_message_content

# Add logo to the sidebar
st.sidebar.image("./logo.png", width=250) 

# Add user mode dropdown to the sidebar
user_mode = st.sidebar.selectbox("Select User Mode", ["TapClicks", "juno"])

CHATBOT_URL = os.getenv("CHATBOT_URL", "http://localhost:8000/rag-agent")
SET_MODE_URL = os.getenv("SET_MODE_URL", "http://localhost:8000/set-mode")

st.title("AIDA Chatbot")
st.info("Ask me a marketing-related question!")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = "default_session_id"

# Send the selected mode to the backend
response = requests.post(SET_MODE_URL, json={"session_id": st.session_state.session_id, "mode": user_mode})
if response.status_code == 200:
    st.sidebar.success(f"Mode set to {user_mode}")
else:
    st.sidebar.error("Failed to set mode")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "output" in message.keys():
            st.markdown(message["output"])

        if "explanation" in message.keys():
            with st.status("How was this generated", state="complete"):
                st.info(message["explanation"])

if prompt := st.chat_input("What do you want to know?"):
    st.chat_message("user").markdown(prompt)

    st.session_state.messages.append({"role": "user", "output": prompt})

    data = {"text": prompt, "session_id": st.session_state.session_id, "mode": user_mode}

    placeholder = st.empty()
    explanation_placeholder = st.empty()
    with st.spinner("Searching for an answer..."):
        streamed_text = ""
        explanation = [] 
        with requests.post(CHATBOT_URL, json=data, stream=True) as response:
            if response.status_code == 200:
                for chunk in response.iter_lines():
                    if chunk:
                        decoded_chunk = chunk.decode('utf-8')
                        message = json.loads(decoded_chunk)
                        if message["type"] == "step":
                            explanation.append(message["content"])
                        elif message["type"] == "output":
                            chatbot_response = parse_message_content(message['content'])
                            streamed_text = chatbot_response['commentary'].replace("$", "\$")
                            placeholder.markdown(streamed_text)
            else:
                output_text = """An error occurred while processing your message.
                Please try again or rephrase your message."""
                placeholder.markdown(output_text)

    chart_data = None
    content = parse_message_content(message['content'])
    if "chart_data" in content:
        chart_data = pd.DataFrame(content["chart_data"])
        chart_data = chart_data.set_index(content["index"])
        chart_type = content["plot"]
        if chart_type == "bar_chart":
            st.bar_chart(chart_data)
        elif chart_type == "line_chart":
            st.line_chart(chart_data)
        elif chart_type == "scatter_chart":
            st.scatter_chart(chart_data)

    st.status("How was this generated", state="complete").info(explanation)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "output": streamed_text,
            "explanation": explanation,
            "chart_data": chart_data.to_dict() if chart_data is not None else None,
        }
    )


# import os
# import json
# import requests
# import numpy as np
# import pandas as pd
# import streamlit as st
# from utility import parse_message_content

# CHATBOT_URL = os.getenv("CHATBOT_URL", "http://localhost:8000/rag-agent")
# SET_MODE_URL = os.getenv("SET_MODE_URL", "http://localhost:8000/set-mode")

# print(os.getcwd())
# st.image("./logo.jpg", width=200)
# st.title("AIDA Chatbot")
# st.info("Ask me a marketing-related question!")

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# if "session_id" not in st.session_state:
#     st.session_state.session_id = "default_session_id"

# # Toggle for user mode
# user_mode = st.selectbox("Select User Mode", ["TapClicks", "juno"])

# # Send the selected mode to the backend
# response = requests.post(SET_MODE_URL, json={"session_id": st.session_state.session_id, "mode": user_mode})
# if response.status_code == 200:
#     st.success(f"Mode set to {user_mode}")
# else:
#     st.error("Failed to set mode")

# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         if "output" in message.keys():
#             st.markdown(message["output"])

#         if "explanation" in message.keys():
#             with st.status("How was this generated", state="complete"):
#                 st.info(message["explanation"])


# if prompt := st.chat_input("What do you want to know?"):
#     st.chat_message("user").markdown(prompt)

#     st.session_state.messages.append({"role": "user", "output": prompt})

#     data = {"text": prompt, "session_id": st.session_state.session_id, "mode": user_mode}

#     placeholder = st.empty()
#     explanation_placeholder = st.empty()
#     with st.spinner("Searching for an answer..."):
#         streamed_text = ""
#         explanation = [] 
#         with requests.post(CHATBOT_URL, json=data, stream=True) as response:
#             if response.status_code == 200:
#                 for chunk in response.iter_lines():
#                     if chunk:
#                         decoded_chunk = chunk.decode('utf-8')
#                         message = json.loads(decoded_chunk)
#                         if message["type"] == "step":
#                             explanation.append(message["content"])
#                         elif message["type"] == "output":
#                             chatbot_response = parse_message_content(message['content'])
#                             streamed_text = chatbot_response['commentary'].replace("$", "\$")
#                             placeholder.markdown(streamed_text)
#             else:
#                 output_text = """An error occurred while processing your message.
#                 Please try again or rephrase your message."""
#                 placeholder.markdown(output_text)

#     chart_data = None
#     content = parse_message_content(message['content'])
#     if "chart_data" in content:
#         chart_data = pd.DataFrame(content["chart_data"])
#         chart_data = chart_data.set_index(content["index"])
#         chart_type = content["plot"]
#         if chart_type == "bar_chart":
#             st.bar_chart(chart_data)
#         elif chart_type == "line_chart":
#             st.line_chart(chart_data)
#         elif chart_type == "scatter_chart":
#             st.scatter_chart(chart_data)

#     st.status("How was this generated", state="complete").info(explanation)

#     st.session_state.messages.append(
#         {
#             "role": "assistant",
#             "output": streamed_text,
#             "explanation": explanation,
#             "chart_data": chart_data.to_dict() if chart_data is not None else None,
#         }
#     )