import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Try to find .env in current or backend dir
load_dotenv()
if not os.getenv("GEMINI_API_KEY"):
    load_dotenv("backend/.env")

api_key = os.getenv("GEMINI_API_KEY")

def test_v1_manual_system(model_id):
    print(f"\n--- Testing {model_id} on v1 with MANUAL System Instruction ---")
    try:
        client = genai.Client(api_key=api_key, http_options={'api_version': 'v1'})
        system_instruction = "You are a helpful assistant."
        user_prompt = "Say hi"
        
        # Manual prepending instead of using system_instruction parameter
        full_prompt = f"SYSTEM: {system_instruction}\n\nUSER: {user_prompt}"
        
        response = client.models.generate_content(
            model=model_id,
            contents=full_prompt
        )
        print(f"✅ SUCCESS: {model_id} on v1 (Manual System Instruction)")
        print(f"   Response: {response.text[:50]}...")
        return True
    except Exception as e:
        print(f"❌ FAILED: {model_id} on v1 - {e}")
        return False

test_v1_manual_system("gemini-1.5-flash")
test_v1_manual_system("gemini-2.0-flash")
