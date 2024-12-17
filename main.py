from openai import OpenAI
import os
import streamlit as st

OPENAI_API_KEY = os.getenv("api_key")
client = OpenAI(api_key=OPENAI_API_KEY)

value = st.chat_input("Votre message ici")

if value:
    with (st.chat_message("user")):
        st.write(value)
    
    with (st.chat_message("assistant")):
        txt = st.header("Waiting for response...")

        completion = client.chat.completions.create(
            model = "gpt-4o-mini",
            messages = [
                {"role" : "user", "content" : value}
            ]
        )

        txt.text(completion.choices[0].message.content)
