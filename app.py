import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai(api_key=os.getenv("OPENAI_API_KEY"))

st.title("Research Assistant")

question = st.text_input("Enter your research question:")

if st.button("Ask"):
    if question:
        try:
            response = client.chat.completions.create(  # Notice the change here
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": question}
                ]
            )
            answer = response.choices[0].message.content.strip() # And here
            st.write(answer)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a question.")