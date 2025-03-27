import streamlit as st
import openai
import os

# Load API key and Assistant ID from .env file
openai_api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("ASSISTANT_ID")

# Set up OpenAI client
client = openai.OpenAI(api_key=openai_api_key)

st.title("Research Assistant")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if user_input := st.chat_input("Ask me anything about research..."):
    # Append user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get response from Assistant
    response = client.beta.threads.create_and_run(
        assistant_id=assistant_id,
        thread={"messages": [{"role": "user", "content": user_input}]}
    )

    # Extract Assistant's reply
    assistant_reply = response.last_run.output["messages"][-1]["content"]

    # Append Assistant's reply to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

    # Display Assistant's reply
    with st.chat_message("assistant"):
        st.markdown(assistant_reply)
