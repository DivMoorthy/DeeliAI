# api.py
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("SECRET_KEY")  # Make sure the key name matches your .env file

# Configure the Gemini API
genai.configure(api_key=api_key)

class API:
    @staticmethod
    def ask_LLM(prompt):
        try:
            # Use the latest Gemini model
            model = genai.GenerativeModel(model_name="models/gemini-2.5-pro")

            # Generate response
            response = model.generate_content(prompt)
            return response.text.strip()

        except Exception as e:
            return f"Error communicating with Gemini API: {e}"
