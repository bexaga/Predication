import streamlit as st
import openai
import json

# Function to call the OpenAI API
def get_openai_completion(user_prompt, system_prompt):
    import os
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "Error: OPENAI_API_KEY is not set in the environment variables."

    openai.api_key = api_key
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=1000  # Limit token usage
        )

        return response

    except openai.error.OpenAIError as e:
        return f"Error: {e}"

# Streamlit UI
st.title("Mon homélie")
st.markdown("Cet assistant vous guide pour identifier un thème, trouver des références et rédiger une homélie personnalisée.")

# Input fields for prompts
system_prompt = st.text_area(
    "System Prompt", 
    "Tu es un assistant qui guide les prédicateurs pour annoncer la Parole de Dieu. Toujours répondre dans ce format JSON strict : {\"options\": [\"Option 1 content\", \"Option 2 content\", \"Option 3 content\"]}."
)
user_prompt = st.text_area("User Prompt", "Propose 3 psaumes sur l'Espérance")

if st.button("Generate Homily"):
    # Fetch completion via OpenAI API
    with st.spinner("Generating homily..."):
        response = get_openai_completion(user_prompt, system_prompt)

        if isinstance(response, str) and response.startswith("Error"):
            st.error(response)
        else:
            try:
                # Parse the response to JSON
                response_content = json.loads(response["choices"][0]["message"]["content"])

                # Ensure the response contains options
                if "options" in response_content and isinstance(response_content["options"], list):
                    st.markdown("### Sélectionnez un ou plusieurs thèmes ci-dessous :")

                    # Generate the selectable options
                    selected_options = st.multiselect(
                        "Options disponibles :",
                        options=[f"( ) Thème {i+1}: {response_content['options'][i]}" for i in range(len(response_content["options"]))]
                    )

                    # Display selected options
                    if selected_options:
                        for option in selected_options:
                            st.markdown(f"**{option}**")
                    else:
                        st.info("Aucune option sélectionnée.")
                else:
                    st.error("La réponse ne contient pas la structure attendue 'options'.")

            except json.JSONDecodeError:
                st.error("Échec de l'analyse de la réponse en JSON. Assurez-vous que l'IA renvoie une structure JSON valide.")
