import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

def list_models(version):
    print(f"\n--- Listing Models (API Version: {version}) ---")
    try:
        client = genai.Client(api_key=api_key, http_options={'api_version': version})
        for model in client.models.list():
            print(f"Name: {model.name}, Supported: {model.supported_generation_methods}")
    except Exception as e:
        print(f"Error ({version}): {e}")

list_models("v1")
list_models("v1beta")
