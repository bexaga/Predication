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
            model="gpt-4",
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
st.title("Homily Assistant")

# Input fields for prompts
system_prompt = st.text_area(
    "System Prompt", 
    "tu assistes les prédicateurs pour annoncer la parole de Dieu. "
    "Toujours répondre dans ce format JSON strict : {\"options\": [\"Option 1 content\", \"Option 2 content\", \"Option 3 content\"]}."
)
user_prompt = st.text_area("User Prompt", "rédige une homélie pour ce jour")

if st.button("Generate Homily"):
    # Fetch completion via OpenAI API
    with st.spinner("Generating homily..."):
        response = get_openai_completion(user_prompt, system_prompt)

        if isinstance(response, str) and response.startswith("Error"):
            st.error(response)
        else:
            try:
                # Print raw response for debugging
                st.write("### Raw Response:")
                st.json(response)

                # Parse the response to JSON
                response_content = json.loads(response["choices"][0]["message"]["content"])

                # Ensure the response contains options
                if "options" in response_content and isinstance(response_content["options"], list):
                    # Use the actual text of each option as the radio button label
                    selected_option = st.radio("Select an option to display:", options=response_content["options"])

                    # Display the selected option
                    st.text_area("Selected Homily Option", value=selected_option, height=200)
                else:
                    st.error("The response does not contain the expected 'options' structure.")

            except json.JSONDecodeError:
                st.error("Failed to parse the response as JSON. Ensure the AI returns a valid JSON structure.")
