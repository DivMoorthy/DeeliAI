# api.py
from key import Key
import google.generativeai as genai

# Set your API key here or load it from environment variable
genai.configure(Key.getKey())  # replace with your actual key or use os.environ

class API:
    @staticmethod
    def ask_LLM(prompt):
        try:
            # Use the latest stable model
            model = genai.GenerativeModel(model_name="models/gemini-2.5-pro")
            
            # Generate response
            response = model.generate_content(prompt)
            return response.text.strip()

        except Exception as e:
            return f"Error communicating with Gemini API: {e}"