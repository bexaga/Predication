from email.message import EmailMessage
import smtplib
from pydantic import BaseModel
import streamlit as st
import openai
from openai import beta
import json
import os
import traceback as tb

OPENAI_MODEL="gpt-4o-mini"
### Streamlit config ###
st.set_page_config(
    page_title="Predication Generator",
    layout="centered",
    menu_items={"About": "bexaga Lab à Genève, contact us at gaillardbx@gmail.com"}
)

### GPT Connection ###
######################
if not os.getenv("OPENAI_API_KEY"):
    st.error("Error: OPENAI_API_KEY is not set in the environment variables.")
client = openai.OpenAI()

# Schemas for GPT JSON structure output
class KeyMessagesSchema(BaseModel):
    """Use this class for JSON structured output as {"key_messages": [msg1, msg2...]}"""
    key_messages: list[str]

def generate_chatgpt_responses(prompt=None, response_format=None):
    """Return the result of asking a simple completion with the system prompt and the passed 
    `prompt`. Can stick to a JSON schema when supplied with a response_format Pydantic class."""
    system_prompts = {
        "English": "You are an assistant that helps preachers find inspiration. Please ALWAYS reply in ENGLISH. Only produce the requested text and avoid openers like 'Certainly! Here’s what you asked {sermon}'. Instead, just output {sermon}",
        "French": "Vous aidez les prédicateurs à trouver l'inspiration. Répondez TOUJOURS en FRANÇAIS. Donnez uniquement le texte demandé et évitez les introductions comme 'Voici ce que vous avez demandé {sermon}'. Juste le texte {sermon}.",
        "Spanish": "Ayudas a los predicadores a encontrar inspiración. Responde SIEMPRE en ESPAÑOL. Solo da el texto solicitado y evita introducciones como 'Aquí tienes lo que pediste {sermón}'. Solo el texto {sermón}."
    }

    system_prompt = system_prompts[st.session_state["LANGUAGE"]]

    messages=[
        {
            "role" : "system",
            "content" : system_prompt
        },
        {
            "role": "user",
            "content": prompt,
        }
    ]

    try:
        if response_format is None:
            response = client.chat.completions.create(
                messages=messages,
                model=OPENAI_MODEL
            )
        else: 
            response = client.beta.chat.completions.parse(
                messages=messages,
                model=OPENAI_MODEL,
                response_format=response_format
            )
        st.text(f"DEBUG: prompting with prompt: {prompt}")
        st.text(f"DEBUG: JSON RETURNED {response.model_dump_json(indent=4)}")
        completion = response.choices[0].message.content.strip()
        
        # Try convertin to JSON if GPT returned a JSON-like object
        try: 
            completion = json.loads(completion)
        except: 
            pass

        return completion
    except Exception as e:
        st.error(tb.format_exc())

# Function to call the OpenAI API
def get_openai_completion(user_prompt, system_prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=1000  # Limit token usage
        )
        return response
    except Exception as e:
        return f"Error: {e}"
### GPT Connection ###

### Streamlit app ###
#####################
# Initialize session state variables so that when the button restarts the page it doesn't lose track of the selections
if "RESPONSES" not in st.session_state: 
    st.session_state["RESPONSES"] = []
if "SELECTED_RESPONSE" not in st.session_state:
    st.session_state["SELECTED_RESPONSE"] = None
if "THEME" not in st.session_state:
    st.session_state["THEME"] = None
if "INSPIRATIONS" not in st.session_state:
    st.session_state["INSPIRATIONS"] = {}
### DEBUG: Initialize session state
if "selected_options" not in st.session_state:
    st.session_state["selected_options"] = []

if "options_text" not in st.session_state:
    st.session_state["options_text"] = {}

# Streamlit UI
st.title("Mon homélie")
st.markdown("Cet assistant vous guide pour identifier un thème, trouver des références et rédiger une homélie personnalisée.")

# # Input fields for prompts
# system_prompt = st.text_area(
#     "System Prompt", 
#     """Tu es un assistant qui guide les prédicateurs pour annoncer la Parole de Dieu. 
#     Lorsque l'utilisateur te pose une question, réponds dans un format JSON strict.
#     Assure-toi que la réponse JSON soit formatée exactement ainsi : 
#     {
#         "options": [
#             "Option 1 content",
#             "Option 2 content",
#             "Option 3 content"
#         ]
#     }.
#     Si le contenu demandé dépasse tes capacités, réponds quand même dans ce format avec des suggestions générales."""
# )

# user_prompt = st.text_area("User Prompt", "Analyse les textes du jour sur aelf.org: première et seconde lecture, évangile, psaume et propose 3 thèmes pour une homélie")

# if st.button("Proposer un thème"):
#     # Fetch completion via OpenAI API
#     with st.spinner("Je prépare 3 options de thèmes."):
#         response = generate_chatgpt_responses(user_prompt, KeyMessagesSchema)

#         if isinstance(response, str) and response.startswith("Error"):
#             st.error(response)
#         else:
#             try:
#                 # Debugging: Show raw response content
#                 st.markdown("### Debug: Raw JSON Response")
#                 st.write(response)

#                 # Parse the response to JSON
#                 response_content = json.loads(response.choices[0].message.content)

#                 # Ensure the response contains options
#                 if "options" in response_content and isinstance(response_content["options"], list):
#                     # Debugging: Show parsed options
#                     st.markdown("### Debug: Parsed Options")
#                     st.write(response_content["options"])

#                     # Store options in session state
#                     st.session_state["options_text"] = {
#                         f"Thème {i+1}": response_content["options"][i] 
#                         for i in range(len(response_content["options"]))
#                     }

#                     # Generate the selectable options
#                     selected_options = st.multiselect(
#                         "Options disponibles (avec texte) :",
#                         options=list(st.session_state["options_text"].keys()),
#                         default=st.session_state["selected_options"]
#                     )

#                     # Update session state with selected options
#                     st.session_state["selected_options"] = selected_options
#                 else:
#                     st.error("La réponse ne contient pas la structure attendue 'options'.")

#             except json.JSONDecodeError:
#                 st.error("Échec de l'analyse de la réponse en JSON. Assurez-vous que l'IA renvoie une structure JSON valide.")

# # Display the text for the selected options
# if st.session_state["selected_options"]:
#     st.markdown("### Vos sélections :")
#     for option in st.session_state["selected_options"]:
#         if option in st.session_state["options_text"]:
#             st.markdown(f"#### {option}")
#             st.write(f"Thème: {st.session_state['options_text'][option]}")
#         else:
#             st.markdown(f"#### {option}")
#             st.write("Texte non disponible")

### Streamlit app setup
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
    theme = st.selectbox("Select Theme", ["Mariage", "Enterrement", "Première Communion", "Confirmation", "Pâques", "Toussaint", "Noël", "Others"], key="THEME")
    if theme == "Others":
        theme = st.text_input("Enter custom theme:", key="THEME")
    topic_prompt = f"Proposer 5 messages clés qui pourraient être le message central d'une homélie sur le thème {theme}."
elif method == "Custom Input":
    topic_prompt = st.text_area("Enter your custom topic prompt:")

if st.button("Generate Key Messages"):
    # Call GPT function
    responses = generate_chatgpt_responses(topic_prompt, KeyMessagesSchema)["key_messages"]

    # Check if GPT returned valid responses
    if responses:
        st.session_state["RESPONSES"] = responses  # Persist responses in session_state
    else:
        st.error("Something went wrong and GPT sent back an empty response.")

# Display generated key messages
if st.session_state["RESPONSES"]:
    st.write("### Choose a Key Message:")
    for i, response in enumerate(st.session_state["RESPONSES"]):
        if st.button(response, key=f"option_{i}"):
            st.session_state["SELECTED_RESPONSE"] = response  # Persist selection
            st.success(f"Selected: {response}")

# Step 2: Generate Inspirations
st.header("Step 2: Generate Inspirations")
if st.session_state["SELECTED_RESPONSE"]:
    # Display Step 2 only if a key message was selected
    st.write(f"Key message selected: **{st.session_state['SELECTED_RESPONSE']}**")
    inspiration_sources = {
        "Joke": "Tu es un pasteur évangélique médiatique, propose 3 mots d'esprit ou blagues sur le thème {theme} en {language}. Tu devrais prendre en compte le message clé suivant pour la prédication : {key_message}.",
        "Semantic Explanation": "Une explication sémantique pour un mot complexe utilisé dans les textes du jour en {language}. Tu devrais prendre en compte le message clé suivant pour la prédication : {key_message}.",
        "Dogma Reference": "Une ouverture sur une référence des textes officiels de la doctrine, catéchisme, pères de l'église en {language}. Tu devrais prendre en compte le message clé suivant pour la prédication : {key_message}.",
        "Current Event": "Un évènement actuel pertinent pour les chrétiens auquel on pourrait faire référence en lien avec {topic} en {language}. Tu devrais prendre en compte le message clé suivant pour la prédication : {key_message}.",
        "Metaphor": "Une métaphore créative pour expliquer {topic} en {language}. Tu devrais prendre en compte le message clé suivant pour la prédication : {key_message}.",
        "Everyday Life Situation": "Une situation de la vie quotidienne où ce message clé sera particulièrement pertinent en {language}. Tu devrais prendre en compte le message clé suivant pour la prédication : {key_message}."
    }
    
    for source, prompt_template in inspiration_sources.items():
        prompt = prompt_template.format(
            theme=st.session_state["THEME"],
            topic=st.session_state["SELECTED_RESPONSE"],
            language=st.session_state["LANGUAGE"],
            key_message=st.session_state["SELECTED_RESPONSE"],
        )
        if st.button(f"Generate {source}", key=f"generate_{source}"):
            # Generate responses for the source
            response = generate_chatgpt_responses(prompt)

            def toggle_inspiration():
                if source in st.session_state["INSPIRATIONS"]:
                    st.session_state["INSPIRATIONS"].pop(source)
                else:
                    st.session_state["INSPIRATIONS"][source] = response

            if response:
                st.session_state["INSPIRATIONS"][source] = response

        if source in st.session_state["INSPIRATIONS"]:
            st.checkbox(f"Include generated {source}: {response}", key=f"INSPIRATION_{source}")
else:
    st.info("Please select a key message in Step 1 to continue.")
    
# Step 3: Compose the Predication
st.header("Step 3: Compose the Predication")
profile = st.selectbox("Who are we writing this for?", ["Prêtre catholique", "Pasteur protestant", "Pasteur évangélique", "Père ou mère de famille"])

if st.button("Generate Predication"):
    predication_prompt = (
        f"Rédige une homélie de 8 minutes pour {profile} en {st.session_state['LANGUAGE']} qui communique sur {st.session_state.get('THEME', '')} et qui inclut comme inspiration:" + json.dumps(st.session_state["INSPIRATIONS"], indent=4)
    )
    # f"en utilisant ces sources: {', '.join(source_variables.values())}."
    predication = generate_chatgpt_responses(predication_prompt)
    st.markdown(predication, unsafe_allow_html=True)

# Step 4: Share
st.header("Step 4: Share")
email = st.text_input("Enter your email address:")
city = st.text_input("City:")
country = st.text_input("Country:")

def send_mail(to_email, subject, message, server='smtp.gmail.com'):
    
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = os.environ.get("EMAIL_USER")
    msg['To'] = ', '.join(to_email)
    msg.set_content(message)
    print(msg)
    server = smtplib.SMTP(server)
    server.set_debuglevel(1)
    server.login(os.environ.get("EMAIL_USER"), os.environ.get("EMAIL_PASSWORD"))  # user & password
    server.send_message(msg)
    server.quit()
    print('successfully sent the mail.')

if st.button("Send Email"):
    send_mail(email, "Your predication for the day", predication)
    # TODO Send email.
### Streamlit app ###