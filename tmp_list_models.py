import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key, http_options={'api_version': 'v1beta'})

print("--- Listing Models (v1beta) ---")
try:
    for model in client.models.list():
        print(f"Name: {model.name}, DisplayName: {model.display_name}, Supported: {model.supported_generation_methods}")
except Exception as e:
    print(f"Error: {e}")
