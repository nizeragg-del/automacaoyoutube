import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

def test_model(model_name, version):
    print(f"Testing {model_name} with version {version}...")
    try:
        client = genai.Client(api_key=api_key, http_options={'api_version': version})
        response = client.models.generate_content(
            model=model_name,
            contents="Say hi"
        )
        print(f"SUCCESS: {model_name} on {version}")
        return True
    except Exception as e:
        print(f"FAILED: {model_name} on {version} - {e}")
        return False

# List models properly
print("--- Listing Models ---")
try:
    client = genai.Client(api_key=api_key)
    for model in client.models.list():
        print(f"Model: {model.name}, Supported: {model.supported_generation_methods}")
except Exception as e:
    print(f"Error listing models: {e}")

# Test some common ones
test_model("gemini-1.5-flash", "v1")
test_model("gemini-1.5-flash", "v1beta")
test_model("gemini-2.0-flash", "v1")
test_model("gemini-2.0-flash", "v1beta")
