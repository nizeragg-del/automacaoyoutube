import base64
import os
from services.ai_engine import AIEngine

def main():
    engine = AIEngine()
    
    idea = "A brave explorer discovering a glowing mystical cave"
    print(f"--- Generating Prompt for: {idea} ---")
    
    prompt = engine.generate_detailed_prompt(idea)
    print(f"Prompt Generated: {prompt[:100]}...")
    
    print("\n--- Generating Image (Flux) ---")
    try:
        image_bytes = engine.generate_image(prompt)
        with open("test_image.jpg", "wb") as f:
            f.write(image_bytes)
        print("Image saved as test_image.jpg")
        
        # Convert to Base64 for Runway
        image_b64 = base64.b64encode(image_bytes).decode('utf-8')
        
        print("\n--- Generating Video (Runway) ---")
        task_id = engine.generate_video_task(image_b64, prompt)
        print(f"Task ID: {task_id}. Waiting for result...")
        
        video_url = engine.get_video_result(task_id)
        print(f"\nSUCCESS! Video URL: {video_url}")
        
    except Exception as e:
        print(f"Error during flow: {e}")
        print("Note: Make sure your API keys are set in .env")

if __name__ == "__main__":
    main()
