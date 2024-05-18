import os
import json
import requests
import streamlit as st

CHATBOT_URL = os.getenv("CHATBOT_URL", "http://localhost:8000/rag-agent")
SET_MODE_URL = os.getenv("SET_MODE_URL", "http://localhost:8000/set-mode")

st.title("RAG Chatbot")
st.info("Ask me a marketing-related question!")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = "default_session_id"

# Toggle for user mode
user_mode = st.selectbox("Select User Mode", ["TapClicks", "Baxter-Auto"])

# Send the selected mode to the backend
response = requests.post(SET_MODE_URL, json={"session_id": st.session_state.session_id, "mode": user_mode})
if response.status_code == 200:
    st.success(f"Mode set to {user_mode}")
else:
    st.error("Failed to set mode")

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
                            streamed_text = message["content"]
                            placeholder.markdown(streamed_text)
            else:
                output_text = """An error occurred while processing your message.
                Please try again or rephrase your message."""
                placeholder.markdown(output_text)

    # explanation = response.json()["intermediate_steps"]
    st.status("How was this generated", state="complete").info(explanation)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "output": streamed_text,
            "explanation": explanation,
        }
    )