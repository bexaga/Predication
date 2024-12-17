import streamlit as st
import openai

# Set up OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]



def generate_chatgpt_responses(prompt):
    """
    Generates a response from ChatGPT using OpenAI's API.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant to help preachers find inspiration."},
                {"role": "user", "content": prompt},
            ],
        )
        # Extract the content of the first response
        return [response["choices"][0]["message"]["content"].strip()]
        print(response)
    except Exception as e:
        print(f"Error generating response: {e}")
        return None

# Set page config
st.set_page_config(
    page_title="Predication Generator",
    layout="centered",
    menu_items={"About": "bexaga Lab à Genève, contact us at gaillardbx@gmail.com"}
)

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
    responses = generate_chatgpt_responses(topic_prompt)
    if responses:
        st.session_state["RESPONSES"] = responses
        st.write("### Choose a Key Message:")
        for i, response in enumerate(responses):
            if st.button(response, key=f"option_{i}"):
                st.session_state["SELECTED_RESPONSE"] = response
                st.success(f"Selected: {response}")

# Step 2: Generate Inspirations
st.header("Step 2: Generate Inspirations")
if "SELECTED_RESPONSE" in st.session_state:
    inspiration_sources = {
        "Joke": "Tu es un pasteur évangélique médiatique, propose 3 mots d'esprit ou blagues sur le thème {theme} en {language}.",
        "Semantic Explanation": "Une explication sémantique pour un mot complexe utilisé dans les textes du jour en {language}.",
        "Dogma Reference": "Une ouverture sur une référence des textes officiels de la doctrine, catéchisme, pères de l'église en {language}.",
        "Current Event": "Un évènement actuel pertinent pour les chrétiens auquel on pourrait faire référence en lien avec {topic} en {language}.",
        "Metaphor": "Une métaphore créative pour expliquer {topic} en {language}.",
        "Everyday Life Situation": "Une situation de la vie quotidienne où ce message clé sera particulièrement pertinent en {language}."
    }

    source_responses = {}
    for source, prompt_template in inspiration_sources.items():
        prompt = prompt_template.format(theme=theme, topic=st.session_state["SELECTED_RESPONSE"], language=language)
        if st.button(f"Generate {source}"):
            response = generate_chatgpt_responses(prompt)
            if response:
                source_responses[source] = response[0]
                st.text_area(f"{source} Output", response[0], height=150, disabled=True)

# Step 3: Compose the Predication
st.header("Step 3: Compose the Predication")
profile = st.selectbox("Who are we writing this for?", ["Prêtre catholique", "Pasteur protestant", "Pasteur évangélique", "Père ou mère de famille"])

if st.button("Generate Predication"):
    selected_topic = st.session_state.get('SELECTED_RESPONSE', '')
    predication_prompt = (
        f"Rédige une homélie de 8 minutes pour {profile} en {language} qui communique sur '{selected_topic}'."
    )
    predication = generate_chatgpt_responses(predication_prompt)
    if predication and len(predication) > 0:
        st.markdown(predication[0], unsafe_allow_html=True)
    else:
        st.error("No predication could be generated. Please try again.")

# Step 4: Share
st.header("Step 4: Share")
email = st.text_input("Enter your email address:")
city = st.text_input("City:")
country = st.text_input("Country:")

if st.button("Send Email"):
    # TODO: Implement the email sending functionality
    st.success("Email sent successfully (dummy action).")
