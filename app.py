import streamlit as st
import openai
import os
import time  # Add this to handle response fetching properly

# Load API key and Assistant ID from environment variables
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

    # Create a new thread for the assistant
    thread = client.beta.threads.create()
    
    # Add the user message to the thread
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input
    )

    # Run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    # Wait for completion
    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run_status.status in ["completed", "failed"]:
            break
        time.sleep(2)  # Wait before checking again

    # Retrieve messages from the thread
    messages = client.beta.threads.messages.list(thread_id=thread.id)

    # Extract the latest assistant response
    assistant_reply = next(
        (msg.content[0].text.value for msg in reversed(messages.data) if msg.role == "assistant"), 
        "I'm sorry, I couldn't generate a response."
    )

    # Append Assistant's reply to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

    # Display Assistant's reply
    with st.chat_message("assistant"):
        st.markdown(assistant_reply)
