import streamlit as st
import openai
from openai import OpenAI

# DEBUG: Start of the app
st.write("DEBUG: Application start")

# Set up OpenAI API key
try:
    st.write("DEBUG: Attempting to retrieve OPENAI_API_KEY")
    api_key = st.secrets["OPENAI_API_KEY"]
    client = OpenAI(api_key=api_key)
    st.write("DEBUG: OPENAI_API_KEY successfully retrieved and client initialized")
except Exception as e:
    st.error(f"DEBUG: Failed to set API key or initialize OpenAI client: {e}")

def generate_chatgpt_responses(prompt):
    """
    Generates a response from ChatGPT (GPT-4) using OpenAI's API.
    """
    st.write("DEBUG: generate_chatgpt_responses called with prompt:", prompt)
    if not prompt:
        st.error("DEBUG: Empty prompt provided to generate_chatgpt_responses.")
        return None
    try:
        st.write("DEBUG: Attempting to call openai.ChatCompletion.create")
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        st.write("DEBUG: Received response from openai.ChatCompletion.create")
        # Extract the content of the first response
        return [response.choices[0].message.content.strip()]
    except Exception as e:
        st.error(f"DEBUG: Error generating response: {e}")
        return None

# Set page config
try:
    st.set_page_config(
        page_title="Predication Generator",
        layout="centered",
        menu_items={"About": "bexaga Lab à Genève, contact us at gaillardbx@gmail.com"}
    )
    st.write("DEBUG: Page config set successfully")
except Exception as e:
    st.error(f"DEBUG: Error setting page config: {e}")

# Hamburger menu
with st.sidebar:
    st.write("DEBUG: Sidebar setup start")
    st.header("Menu")
    language = st.selectbox("Select Language", ["French", "English", "Spanish"], key="LANGUAGE")
    st.markdown("**About Us**: bexaga Lab à Genève\n**Contact Us**: gaillardbx@gmail.com")
    st.write("DEBUG: Sidebar setup complete with language:", language)

# Step 1: Identify Key Message
st.header("Step 1: Identify Key Message")
method = st.radio("Choose a method to identify the key message:", ["No Input", "Select a Theme", "Custom Input"], key="METHOD")
st.write("DEBUG: Method selected:", method)

theme = ""
topic_prompt = ""
if method == "No Input":
    st.write("DEBUG: Method == No Input")
    topic_prompt = "Identifier l'évangile du jour, les lectures de l'ancien testament et du nouveau testament, du psaume. Proposer 5 messages clés qui pourraient être le message central de l'homélie du jour."
elif method == "Select a Theme":
    st.write("DEBUG: Method == Select a Theme")
    theme = st.selectbox("Select Theme", ["Mariage", "Enterrement", "Première Communion", "Confirmation", "Pâques", "Toussaint", "Noël", "Others"])
    st.write("DEBUG: Theme selected:", theme)
    if theme == "Others":
        theme = st.text_input("Enter custom theme:")
        st.write("DEBUG: Custom theme input:", theme)
    topic_prompt = f"Proposer 5 messages clés qui pourraient être le message central d'une homélie sur le thème {theme}."
elif method == "Custom Input":
    st.write("DEBUG: Method == Custom Input")
    topic_prompt = st.text_area("Enter your custom topic prompt:")
    st.write("DEBUG: Custom topic prompt:", topic_prompt)

if st.button("Generate Key Messages"):
    st.write("DEBUG: 'Generate Key Messages' button clicked")
    if not topic_prompt:
        st.error("DEBUG: No topic prompt provided for key message generation.")
    responses = generate_chatgpt_responses(topic_prompt)
    if responses:
        st.write("DEBUG: Responses received for key messages:", responses)
        st.session_state["RESPONSES"] = responses
        st.write("### Choose a Key Message:")
        for i, response in enumerate(responses):
            if st.button(response, key=f"option_{i}"):
                st.session_state["SELECTED_RESPONSE"] = response
                st.success(f"Selected: {response}")
                st.write("DEBUG: Response selected:", response)
    else:
        st.error("DEBUG: No responses returned for the key messages.")

# Step 2: Generate Inspirations
st.header("Step 2: Generate Inspirations")
if "SELECTED_RESPONSE" in st.session_state:
    st.write("DEBUG: SELECTED_RESPONSE exists:", st.session_state["SELECTED_RESPONSE"])
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
        st.write(f"DEBUG: Generating inspiration for source: {source} with prompt: {prompt}")
        if st.button(f"Generate {source}"):
            st.write("DEBUG: Button clicked for:", source)
            response = generate_chatgpt_responses(prompt)
            if response:
                source_responses[source] = response[0]
                st.text_area(f"{source} Output", response[0], height=150, disabled=True)
                st.write("DEBUG: Inspiration response received for", source, ":", response[0])
            else:
                st.error(f"DEBUG: No response received for {source} inspiration.")
else:
    st.write("DEBUG: No SELECTED_RESPONSE found, cannot generate inspirations.")

# Step 3: Compose the Predication
st.header("Step 3: Compose the Predication")
profile = st.selectbox("Who are we writing this for?", ["Prêtre catholique", "Pasteur protestant", "Pasteur évangélique", "Père ou mère de famille"])
st.write("DEBUG: Profile selected:", profile)

if st.button("Generate Predication"):
    st.write("DEBUG: 'Generate Predication' button clicked")
    selected_topic = st.session_state.get('SELECTED_RESPONSE', '')
    st.write("DEBUG: Selected topic for predication:", selected_topic)
    predication_prompt = (
        f"Rédige une homélie de 8 minutes pour {profile} en {language} qui communique sur '{selected_topic}'."
    )
    st.write("DEBUG: Predication prompt:", predication_prompt)
    predication = generate_chatgpt_responses(predication_prompt)
    if predication and len(predication) > 0:
        st.write("DEBUG: Predication generated successfully")
        st.markdown(predication[0], unsafe_allow_html=True)
    else:
        st.error("DEBUG: No predication could be generated. Please try again.")

# Step 4: Share
st.header("Step 4: Share")
email = st.text_input("Enter your email address:")
city = st.text_input("City:")
country = st.text_input("Country:")

st.write("DEBUG: Share data - email:", email, "city:", city, "country:", country)
if st.button("Send Email"):
    # TODO: Implement the email sending functionality
    st.success("DEBUG: Email sent successfully (dummy action).")
    st.write("DEBUG: 'Send Email' button clicked, no actual email sent.")
