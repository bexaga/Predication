import streamlit as st
import openai
import re
from email_validator import validate_email, EmailNotValidError

#pip install --upgrade openai


# Set up OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

def validate_email_address(email):
    try:
        valid = validate_email(email)
        return valid.email
    except EmailNotValidError as e:
        return None

def generate_chatgpt_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Use the latest chat model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return None


# Set page config
st.set_page_config(page_title="Predication Generator", layout="centered", menu_items={"About": "bexaga Lab à Genève, contact us at gaillardbx@gmail.com"})

# Hamburger menu
with st.sidebar:
    st.header("Menu")
    language = st.selectbox("Select Language", ["French", "English", "Spanish"], key="LANGUAGE")
    st.markdown("**About Us**: bexaga Lab à Genève\n**Contact Us**: gaillardbx@gmail.com")

# Step 1: Identify Key Message
st.header("Step 1: Identify Key Message")
method = st.radio("Choose a method to identify the key message:", ["No Input", "Select a Theme", "Custom Input"], key="METHOD")

theme = ""
topic_prompt = ""
if method == "No Input":
    topic_prompt = "Identifier l'évangile du jour, les lectures de l'ancien testament et du nouveau testament, du psaume. Proposer 5 messages clés qui pourraient être le message central de l'homélie du jour."
elif method == "Select a Theme":
    theme = st.selectbox("Select Theme", ["Mariage", "Enterrement", "Première Communion", "Confirmation", "Pâques", "Toussaint", "Noël", "Others"])
    if theme == "Others":
        theme = st.text_input("Enter custom theme:")
    topic_prompt = f"Proposer 5 messages clés qui pourraient être le message central d'une homélie sur le thème {theme}."
elif method == "Custom Input":
    topic_prompt = st.text_area("Enter your custom topic prompt:")

if st.button("Generate Key Messages"):
    topic = generate_chatgpt_response(topic_prompt)
    st.session_state["TOPIC"] = topic
    st.text_area("Key Messages", topic, height=200, disabled=True)

# Step 2: Generate Inspirations
st.header("Step 2: Generate Inspirations")
source_variables = {}

inspiration_sources = {
    "Joke": "Tu es un pasteur évangélique médiatique, propose 3 mots d'esprit ou blagues sur le thème {theme} en {language}.",
    "Semantic Explanation": "Une explication sémantique pour un mot complexe utilisé dans les textes du jour en {language}.",
    "Dogma Reference": "Une ouverture sur une référence des textes officiels de la doctrine, catéchisme, pères de l'église en {language}.",
    "Current Event": "Un évènement actuel pertinent pour les chrétiens auquel on pourrait faire référence en lien avec {topic} en {language}.",
    "Metaphor": "Une métaphore créative pour expliquer {topic} en {language}.",
    "Everyday Life Situation": "Une situation de la vie quotidienne où ce message clé sera particulièrement pertinent en {language}."
}

for source, prompt_template in inspiration_sources.items():
    st.subheader(source)
    prompt = prompt_template.format(theme=theme, topic=st.session_state.get("TOPIC", ""), language=language)
    if st.button(f"Generate {source}"):
        response = generate_chatgpt_response(prompt)
        source_variables[source] = response
        st.session_state[f"SOURCE_{source.upper().replace(' ', '_')}"] = response
        st.text_area(f"{source} Output", response, height=150, disabled=True)

# Step 3: Compose the Predication
st.header("Step 3: Compose the Predication")
profile = st.selectbox("Who are we writing this for?", ["Prêtre catholique", "Pasteur protestant", "Pasteur évangélique", "Père ou mère de famille"])

if st.button("Generate Predication"):
    predication_prompt = (
        f"Rédige une homélie de 8 minutes pour {profile} en {language} qui communique sur {st.session_state.get('TOPIC', '')} "
        f"en utilisant ces sources: {', '.join(source_variables.values())}."
    )
    predication = generate_chatgpt_response(predication_prompt)
    st.markdown(predication, unsafe_allow_html=True)

# Step 4: Share
st.header("Step 4: Share")
email = st.text_input("Enter your email address:")
city = st.text_input("City:")
country = st.text_input("Country:")

if st.button("Send Email"):
    if validate_email_address(email):
        st.success("Predication emailed successfully!")
    else:
        st.error("Invalid email address. Please enter a valid email.")
