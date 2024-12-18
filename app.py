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
def main():
    st.title("Mon homélie")
    st.markdown("Cet assistant vous guide pour identifier un thème, trouver des références et rédiger une homélie personnalisée.")

    # Input fields for prompts
    system_prompt = st.text_area(
        "System Prompt", 
        "Tu es un assistant qui guide les prédicateurs pour annoncer la Parole de Dieu. Toujours répondre dans ce format JSON strict : {\"options\": [\"Option 1 content\", \"Option 2 content\", \"Option 3 content\"]}."
    )
    user_prompt = st.text_area("User Prompt", "Propose 3 psaumes sur l'Espérance")

    if st.button("Générer les thèmes"):
        # Reset session state for theme selection
        st.session_state.theme_options = None
        st.session_state.selected_themes = []

        # Fetch completion via OpenAI API
        with st.spinner("Génération des thèmes..."):
            response = get_openai_completion(user_prompt, system_prompt)
            if isinstance(response, str) and response.startswith("Error"):
                st.error(response)
            else:
                try:
                    # Parse the response to JSON
                    response_content = json.loads(response["choices"][0]["message"]["content"])
                    
                    # Ensure the response contains options
                    if "options" in response_content and isinstance(response_content["options"], list):
                        # Store options in session state
                        st.session_state.theme_options = response_content["options"]
                        st.experimental_rerun()
                    else:
                        st.error("La réponse ne contient pas la structure attendue 'options'.")
                except json.JSONDecodeError:
                    st.error("Échec de l'analyse de la réponse en JSON. Assurez-vous que l'IA renvoie une structure JSON valide.")

    # Display theme selection or selected themes
    if hasattr(st.session_state, 'theme_options') and st.session_state.theme_options:
        st.markdown("### Sélectionnez un ou plusieurs thèmes :")
        
        # Multiselect for themes
        selected_themes = st.multiselect(
            "Options disponibles :",
            options=[f"Thème {i+1}" for i in range(len(st.session_state.theme_options))]
        )

        # Button to confirm theme selection
        if st.button("Confirmer la sélection"):
            # Store selected themes in session state
            st.session_state.selected_themes = selected_themes

    # Display selected themes
    if hasattr(st.session_state, 'selected_themes') and st.session_state.selected_themes:
        st.markdown("## Thèmes sélectionnés :")
        for option in st.session_state.selected_themes:
            # Extract index from the theme label
            index = int(option.split()[1]) - 1
            st.markdown(f"### {option}")
            st.write(st.session_state.theme_options[index])

# Run the main function
if __name__ == "__main__":
    main()
