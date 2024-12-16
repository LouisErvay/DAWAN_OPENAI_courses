from openai import OpenAI
import os
import streamlit as st

OPENAI_API_KEY = os.getenv("api_key")
client = OpenAI(api_key=OPENAI_API_KEY)

completion = client.chat.completions.create(
    model = "gpt-4o-mini",
    messages = [
        {"role" : "user", "content" : "Hello world"}
    ]
)

print(completion)

st.write("Hello world")