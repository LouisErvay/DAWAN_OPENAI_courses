import streamlit as st

path = "./pages/"
pg = st.navigation([
    st.Page(path + "Home.py", title="1. Home"),
    st.Page(path + "DALL-E.py", title="2. API DALL-E 2"),
    st.Page(path + "Article.py", title="3. Génération d'articles")
])

pg.run()