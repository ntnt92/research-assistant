import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key and Assistant ID from .env
openai.api_key = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

st.title("🧠 Research Assistant")
st.write("Ask your AI-powered assistant anything about research!")

query = st.text_input("Enter your research question:")

if st.button("Ask"):
    if query:
        try:
            # Create a new thread and run assistant
            response = openai.beta.threads.create_and_run(
                assistant_id=ASSISTANT_ID,
                thread={"messages": [{"role": "user", "content": query}]}
            )

            # Extract response from OpenAI API
            assistant_response = response["latest_message"]["content"]
            st.success(assistant_response)

        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a question!")
