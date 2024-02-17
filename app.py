import streamlit as st
from langchain.chat_models import ChatMistralAI  # Updated import
from langchain import hub
import os

# Ensure you have your Mistral API Key set as an environment variable or pass it directly
mistral_api_key = os.getenv('MISTRAL_API_KEY')

st.title("Ditch the Boring Press Releases. Chat with HugPR Instead.")

st.info("""
Your curious new AI buddy for all things Hugging Face Assistants. Ask away, let's talk tech!
""")

if st.button("Ask HugPR"):  # Assuming 'button_text' variable was meant to be the button label
    try:
        # Prompt
        prompt = hub.pull("flflo/hugpr")

        # LLM - Updated to use ChatMistralAI
        model = ChatMistralAI(mistral_api_key=mistral_api_key)

        # Chain
        runnable = prompt | model

        # Invocation - Assuming 'invoke' method structure is similar and 'article_text' is pre-defined
        output = runnable.invoke({"text": "Ask me questions about HuggingChat Assistants!"})  # Update according to your input structure

        # Affichage
        st.write("Output:", output.content)
    except Exception as e:
        st.write(f"An error occurred: {e}")
