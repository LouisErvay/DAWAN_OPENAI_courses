from openai import OpenAI
import os
import streamlit as st

OPENAI_API_KEY = os.getenv("api_key")
client = OpenAI(api_key=OPENAI_API_KEY)

if "article_messages" not in st.session_state:
    st.session_state.article_messages = []

def generate_article_with_titles(topic):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who writes articles with concise paragraphs and meaningful titles."},
            {"role": "user", "content": f"Write an article about: {topic}. Include 2-3 paragraphs with short titles for each paragraph."}
        ]
    )
    return response.choices[0].message.content

def generate_image(topic):
    response = client.images.generate(
        model="dall-e-2",
        prompt=f"A visually appealing and relevant image about {topic}",
        n=1,
        size="256x256"
    )
    return response.data[0].url

st.title("Article Generator")
for message in st.session_state.article_messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            st.write(message["content"])
            if "image_url" in message:
                st.image(message["image_url"], caption="Generated Image")
        else:
            st.write(message["content"])

topic = st.chat_input("Enter a topic for your article")
if topic:
    with st.chat_message("user"):
        st.write(topic)
    st.session_state.article_messages.append({"role": "user", "content": topic})
    with st.chat_message("assistant"):
        st.write("Generating article and image...")
    try:
        article_content = generate_article_with_titles(topic)
        image_url = generate_image(topic)
        with st.chat_message("assistant"):
            paragraphs = article_content.split("\n\n")
            for paragraph in paragraphs:
                if ": " in paragraph:
                    title, content = paragraph.split(": ", 1)
                    st.subheader(title.strip())
                    st.write(content.strip())
                else:
                    st.write(paragraph.strip())
            st.image(image_url, caption="Generated Image")
        st.session_state.article_messages.append({
            "role": "assistant",
            "content": article_content,
            "image_url": image_url
        })
    except Exception as e:
        st.error(f"Error: {e}")
