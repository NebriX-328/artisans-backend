import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env variables
load_dotenv()

AI_API_KEY = os.getenv("AI_API_KEY")
if not AI_API_KEY:
    raise ValueError("Error: AI_API_KEY not found in .env file.")

genai.configure(api_key=AI_API_KEY)

def get_gemini_model():
    # Replace this with your actual model initialization if needed
    return genai
