import streamlit as st
from openai import OpenAI
import os
import json

from assistant import interact_with_assistant, create_thread

OPENAI_API_KEY = os.getenv("api_key")
client = OpenAI(api_key=OPENAI_API_KEY)

# Initialisation des états de session
if "messages_history" not in st.session_state:
    st.session_state.messages_history = []
if "propositions" not in st.session_state:
    st.session_state.propositions = []

# Création des threads
my_thread_id_1 = create_thread()
my_thread_id_2 = create_thread()

st.title("History")


# Fonction pour traiter un nouveau message
def new_message(content: str):
    with st.chat_message("user"):
        st.session_state.messages_history.append({"role": "user", "content": content})
        st.write(content)
    
    assistant_placeholder = st.chat_message("assistant")
    with assistant_placeholder:
        placeholder = st.empty()
        placeholder.write("Waiting for response...")

        try:
            # Interaction avec le premier assistant
            response = interact_with_assistant("asst_3AIMGUBAKSkfTThju2Qs4oWR", content, my_thread_id=my_thread_id_1)

            st.session_state.messages_history.append({"role": "assistant", "content": response})
            placeholder.markdown(response)

            # Interaction avec le second assistant pour obtenir les propositions
            data = json.loads(interact_with_assistant("asst_2xOPDDd9u3OBaMG8Qa1gNMyB", response, my_thread_id=my_thread_id_2))            

            # Mise à jour des propositions
            propositions = [value for key, value in data.items()]
            st.session_state.propositions = propositions

        except Exception as e:
            placeholder.error(f"Error: {e}")

# Affichage des messages dans l'historique
for message in st.session_state.messages_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Affichage de la radio pour sélectionner une proposition si disponible
if st.session_state.propositions:
    st.write("Choisissez la prochaine étape de l'histoire :")
    selected_option = st.radio(
        "Propositions",
        st.session_state.propositions,
        key="radio_propositions",
        index=0
    )

    # Bouton pour confirmer le choix
    if st.button("Confirmer votre choix"):
        new_message(selected_option)

# Champ d'entrée pour un nouveau message utilisateur
value = st.chat_input("Your message here")
if value:
    new_message(value)
