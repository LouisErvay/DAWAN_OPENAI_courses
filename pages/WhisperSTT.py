from openai import OpenAI
import streamlit as st
from pathlib import Path

client = OpenAI()

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

    st.write(transcript.text)

    with open(file_path, "rb") as f:
        translation = client.audio.translations.create(
        file=f,
        model="whisper-1"
        )

    st.write(translation.text)