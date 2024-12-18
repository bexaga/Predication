import streamlit as st
import openai

# Function to call the OpenAI API
def get_openai_completion(user_prompt, system_prompt, api_key):
    openai.api_key = api_key
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            stream=True  # Enable streaming
        )

        return response

    except openai.error.OpenAIError as e:
        return f"Error: {e}"

# Streamlit UI
st.title("Homily Assistant")

# Input fields for prompts and API key
system_prompt = st.text_area("System Prompt", "tu assistes les predicateurs pour annoncer la parole de Dieu")
user_prompt = st.text_area("User Prompt", "redige une homelie pour ce jour")
api_key = 'OPENAI_API_KEY'

if st.button("Generate Homily"):
    if not api_key:
        st.error("Please provide your OpenAI API key.")
    else:
        # Fetch completion via OpenAI API
        with st.spinner("Generating homily..."):
            response = get_openai_completion(user_prompt, system_prompt, api_key)

            if isinstance(response, str) and response.startswith("Error"):
                st.error(response)
            else:
                st.write("### Generated Homily:")
                
                # Stream the response
                for chunk in response:
                    if 'choices' in chunk:
                        message_chunk = chunk['choices'][0]['delta'].get('content', '')
                        if message_chunk:
                            st.write(message_chunk, unsafe_allow_html=True)
