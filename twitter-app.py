import streamlit as st
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain import hub
import requests
from newspaper import Article
import os

lang_choice = st.radio("", ["English", "Français"],horizontal=True)
button_text = "Run" if lang_choice == "English" else "Exécuter"
title_text = "AI-assisted Twitter Thread Generator 📰✨🧵" if lang_choice == "English" else "Générateur de fils Twitter assisté par IA 📰✨🧵"
st.title(title_text)

if lang_choice == "English":
    st.info("""
    A simple tool to ~~flood the Internet~~ generate a Twitter thread (or the 24th letter of the alphabet) from news articles and an opportunity to test LangChain Hub for prompts.
    This project utilizes several technologies:
    - **Streamlit** for the user interface.
    - **OpenAI GPT-3.5 Turbo** for text generation.
    - **LangChain Hub** for accessing predefined models and prompts.
    - **Newspaper3k** for online article scraping.
    Enter the URL of an article along with other parameters, then click 'Run' to get a summarized set of tweets.
    """)
    api_key = st.text_input("Your OpenAI API key", type="password")
    article_url = st.text_input("Article URL")
    language = st.text_input("Language")
    target_audience = st.text_input("Target Audience")
    word_count = st.slider("Word Count", min_value=10, max_value=100, value=30)
    number_of_tweets = st.slider("Number of Tweets", min_value=1, max_value=10, value=3)

else:
    st.info("""
    Un outil simple pour ~~inonder Internet~~ générer un fil Twitter (ou la 24ème lettre de l'alphabet) à partir d'articles de nouvelles et l'occasion de tester LangChain Hub pour les prompts.
    Ce projet utilise :
    - **Streamlit** pour l'interface utilisateur.
    - **OpenAI GPT-3.5 Turbo** pour la génération de texte.
    - **LangChain Hub** pour l'accès à des modèles et prompts prédéfinis.
    - **Newspaper3k** pour l'extraction d'articles en ligne.
    Entrez l'URL d'un article et les autres paramètres, puis cliquez sur 'Exécuter' pour obtenir un résumé sous forme de tweets.
    """)
    api_key = st.text_input("Votre clé d'API OpenAI API", type="password")
    article_url = st.text_input("L'URL de l'article")
    language = st.text_input("Langue")
    target_audience = st.text_input("Public cible")
    word_count = st.slider("Nombre de mots", min_value=10, max_value=100, value=30)
    number_of_tweets = st.slider("Nombre de tweets", min_value=1, max_value=10, value=3)

if st.button(button_text):
    headers = {'User-Agent': 'Mozilla/5.0'}
    session = requests.Session()

    try:
        # Récupérer l'article
        response = session.get(article_url, headers=headers, timeout=10)
        if response.status_code == 200:
            article = Article(article_url)
            article.download()
            article.parse()

            # Prompt
            prompt = hub.pull("flflo/summarization")

            # LLM
            model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=api_key)

            # Chain
            runnable = prompt | model

            # Texte de l'article
            article_text = "Titre: " + article.title + " - Texte: " + article.text

            # Invocation
            output = runnable.invoke({"target_audience": target_audience, "language": language, "text": article_text, "word_count": word_count, "number_of_tweets": number_of_tweets})

            # Affichage
            st.write("Output:", output.content)
        else:
            st.write("Échec de la récupération de l'article.")
    except Exception as e:
        st.write(f"Une erreur s'est produite : {e}")
