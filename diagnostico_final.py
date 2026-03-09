import os
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

def test_config(model_id, version):
    print(f"\n--- Testing {model_id} on {version} ---")
    try:
        client = genai.Client(api_key=api_key, http_options={'api_version': version})
        response = client.models.generate_content(
            model=model_id,
            contents="Diga 'Olá'"
        )
        print(f"✅ SUCCESS: {model_id} on {version}")
        return True
    except Exception as e:
        error_msg = str(e)
        print(f"❌ FAILED: {model_id} on {version}")
        if "429" in error_msg:
            print("   Reason: 429 RESOURCE_EXHAUSTED (Quota issue)")
        elif "404" in error_msg:
            print("   Reason: 404 NOT_FOUND (Model/Version mismatch)")
        elif "400" in error_msg:
            print(f"   Reason: 400 INVALID_ARGUMENT (Payload issue: {error_msg[:100]})")
        else:
            print(f"   Reason: {error_msg}")
        return False

models = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"]
versions = ["v1", "v1beta"]

for model in models:
    for version in versions:
        test_config(model, version)
