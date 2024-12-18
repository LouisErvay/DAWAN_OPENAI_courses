from openai import OpenAI
import os
import streamlit as st
from pathlib import Path

OPENAI_API_KEY = os.getenv("api_key")
client = OpenAI(api_key=OPENAI_API_KEY)


if "messages" not in st.session_state:
    st.session_state.messages = []


def new_message(content: str):
    with st.chat_message("user"):
        st.session_state.messages.append({"role": "user", "content": content})
        st.write(content)

    with st.chat_message("assistant"):
        st.write("Waiting for response...")
        
        try:
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": content}
                ]
            )

            response = completion.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write(response)

        except Exception as e:
            st.error(f"Error: {e}")

audio = st.audio_input("Audio Input")

if (audio):
    file_path = Path(__file__).parent / "audio.mp3"

    with open(file_path, "wb") as f:
        f.write(audio.getbuffer())

    with open(file_path, "rb") as f:
        transcript = client.audio.transcriptions.create(
        file=file_path,
        model="whisper-1"
        )

    new_message(transcript.text)

# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.write(message["content"])

value = st.chat_input("Your message here")
if value:
    new_message(value)
