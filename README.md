# Predication Generator

This assists the preacher with identifying an idea and finding inspiration. We do propose an automated predication but the main value is in browsing options for each source and composing the perfect predication for a given occasion.

This repository contains a Streamlit application designed to help users create personalized predications (homilies) using OpenAI's GPT API. The app guides users through a structured multi-step process to generate, refine, and share predications based on their preferences.

## Features

- **Multi-Language Support**: Select your preferred language for prompts and outputs.
- **Customizable Key Messages**: Identify the central topic of the predication using different methods.
- **Inspiration Sources**: Generate creative content using multiple sources such as jokes, metaphors, and dogma references.
- **Predication Composition**: Tailor the homily to a specific audience profile.
- **Shareable Output**: Share the generated predication via email with options for daily subscriptions.

## Requirements

- Python 3.9+
- Streamlit
- OpenAI Python SDK
- Email Validator

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/predication-generator.git
   cd predication-generator
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your OpenAI API key:
   - Add your OpenAI API key to a `.streamlit/secrets.toml` file:
     ```toml
     [secrets]
     OPENAI_API_KEY = "your-openai-api-key"
     ```

## Running the App

Start the Streamlit app:
```bash
streamlit run app.py
```

The app will open in your web browser. Follow the step-by-step process to generate predications.

## File Structure

- `app.py`: Main application script.
- `requirements.txt`: List of required Python packages.
- `.streamlit/secrets.toml`: File to store secret keys (not included, must be created by the user).
- `README.md`: Documentation for the repository.

## Deployment

To deploy this app to a hosting service like Streamlit Cloud or Heroku, follow these steps:

1. Push the repository to GitHub:
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. Link the repository to your hosting platform and set environment variables for `OPENAI_API_KEY`.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For questions or support, contact us at gaillardbx@gmail.com.
