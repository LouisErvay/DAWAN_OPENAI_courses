import streamlit as st

path = "./pages/"
pg = st.navigation([
    st.Page(path + "Home.py", title="1. Home"),
    st.Page(path + "DALL-E.py", title="2. API DALL-E 2"),
    st.Page(path + "Article.py", title="3. Génération d'articles"),
    st.Page(path + "WhisperSTT.py", title="4. API Whisper - STT"),
    st.Page(path + "WhisperTTS.py", title="5. API Whisper - TTS"),
])

pg.run()