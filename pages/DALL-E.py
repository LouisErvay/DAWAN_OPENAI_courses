from openai import OpenAI
import os
import streamlit as st

API_KEY = os.getenv("api_key")
client = OpenAI(api_key=API_KEY)

if "dalle_message" not in st.session_state:
    st.session_state.dalle_message = []

def openai_create_image(content):
    with st.chat_message("user"):
        st.session_state.dalle_message.append({"role": "user", "content": content})
        st.write(content)

    with st.chat_message("assistant"):
        st.write("Waiting for an answer...")

        try:
            response = client.images.generate(
                model="dall-e-2",
                prompt=content,
                n=1,
                size="256x256"
            )

            image_url = response.data[0].url
            st.session_state.dalle_message.append({"role": "assistant", "content": image_url})
            st.image(image_url)

        except Exception as e:
            st.error(f"Error: {e}")

def openai_create_image_variation(image, content):
    with st.chat_message("user"):
        st.session_state.dalle_message.append({"role": "user", "content": content})
        st.session_state.dalle_message.append({"role": "user", "content": image.name})
        st.write(content)
        st.image(image)

    with st.chat_message("assistant"):
        st.write("Waiting for an answer...")

        try:
            response = client.images.create_variation(
                image=image.read(),
                n=1,
                size="256x256"
            )

            image_url = response.data[0].url
            st.session_state.dalle_message.append({"role": "assistant", "content": image_url})
            st.image(image_url)

        except Exception as e:
            st.error(f"Error: {e}")

for message in st.session_state.dalle_message:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant" and message["content"].startswith("http"):
            st.image(message["content"])
        else:
            st.write(message["content"])

value = st.chat_input("Say something")
uploaded_file = st.file_uploader("Choose a file")

if value and uploaded_file:
    openai_create_image_variation(uploaded_file, value)
    value = ""

if value and not uploaded_file:
    openai_create_image(value)
    value = ""
