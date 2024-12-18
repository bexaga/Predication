import streamlit as st
import openai
import json
import os
import traceback as tb
client = openai.OpenAI()

if not os.getenv("OPENAI_API_KEY"):
    st.error("Error: OPENAI_API_KEY is not set in the environment variables.")


def generate_chatgpt_responses(prompt=None, response_format=None):
    """Return the result of asking a simple completion with the system prompt and the passed `prompt`. Can stick to a JSON schema when supplied with a response_format Pydantic class."""
    
    system_prompts = {
        "English": "You are an assistant that helps preachers find inspiration. Please ALWAYS reply in ENGLISH.",
        "French": "Vous êtes un assistant qui aide les prédicateurs à trouver l'inspiration. Veuillez TOUJOURS répondre en FRANÇAIS.",
        "Spanish": "Eres un asistente que ayuda a los predicadores a encontrar inspiración. Por favor, responde SIEMPRE en ESPAÑOL."
    }
    try:
        system_prompt = system_prompts[st.session_state["LANGUAGE"]]
        response = client.chat.completions.create(
            messages=[
                {
                    "role" : "system",
                    "content" : system_prompt
                },
                {
                    "role": "user",
                    "content": "Say this is a test",
                }
            ],
            model="gpt-4o-mini",
        )
        st.text_input(f"DEBUG: JSON RETURNED {response.model_dump_json(indent=4)}")
        return response.choices[0].message.content.strip()
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

# Initialize session state
if "selected_options" not in st.session_state:
    st.session_state["selected_options"] = []

if "options_text" not in st.session_state:
    st.session_state["options_text"] = {}

# Streamlit UI
st.title("Mon homélie")
st.markdown("Cet assistant vous guide pour identifier un thème, trouver des références et rédiger une homélie personnalisée.")

# Input fields for prompts
system_prompt = st.text_area(
    "System Prompt", 
    """Tu es un assistant qui guide les prédicateurs pour annoncer la Parole de Dieu. 
    Lorsque l'utilisateur te pose une question, réponds dans un format JSON strict.
    Assure-toi que la réponse JSON soit formatée exactement ainsi : 
    {
        "options": [
            "Option 1 content",
            "Option 2 content",
            "Option 3 content"
        ]
    }.
    Si le contenu demandé dépasse tes capacités, réponds quand même dans ce format avec des suggestions générales."""
)

user_prompt = st.text_area("User Prompt", "Analyse les textes du jour sur aelf.org: première et seconde lecture, évangile, psaume et propose 3 thèmes pour une homélie")

if st.button("Proposer un thème"):
    # Fetch completion via OpenAI API
    with st.spinner("Je prépare 3 options de thèmes."):
        response = get_openai_completion(user_prompt, system_prompt)

        if isinstance(response, str) and response.startswith("Error"):
            st.error(response)
        else:
            try:
                # Debugging: Show raw response content
                st.markdown("### Debug: Raw JSON Response")
                st.write(response)

                # Parse the response to JSON
                response_content = json.loads(response.choices[0].message.content)

                # Ensure the response contains options
                if "options" in response_content and isinstance(response_content["options"], list):
                    # Debugging: Show parsed options
                    st.markdown("### Debug: Parsed Options")
                    st.write(response_content["options"])

                    # Store options in session state
                    st.session_state["options_text"] = {
                        f"Thème {i+1}": response_content["options"][i] 
                        for i in range(len(response_content["options"]))
                    }

                    # Generate the selectable options
                    selected_options = st.multiselect(
                        "Options disponibles (avec texte) :",
                        options=list(st.session_state["options_text"].keys()),
                        default=st.session_state["selected_options"]
                    )

                    # Update session state with selected options
                    st.session_state["selected_options"] = selected_options
                else:
                    st.error("La réponse ne contient pas la structure attendue 'options'.")

            except json.JSONDecodeError:
                st.error("Échec de l'analyse de la réponse en JSON. Assurez-vous que l'IA renvoie une structure JSON valide.")

# Display the text for the selected options
if st.session_state["selected_options"]:
    st.markdown("### Vos sélections :")
    for option in st.session_state["selected_options"]:
        if option in st.session_state["options_text"]:
            st.markdown(f"#### {option}")
            st.write(f"Thème: {st.session_state['options_text'][option]}")
        else:
            st.markdown(f"#### {option}")
            st.write("Texte non disponible")
