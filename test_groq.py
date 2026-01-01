import httpx
import json
import os

async def test_groq_api():
    api_key = os.getenv("GROQ_API_KEY", "your_groq_api_key_here")
    
    # Test different models
    models_to_test = [
        "llama3-8b-8192",
        "llama3-70b-8192", 
        "llama-3.1-8b-instant",
        "llama-3.1-70b-versatile",
        "llama-3.2-1b-preview",
        "llama-3.2-3b-preview",
        "mixtral-8x7b-32768",
        "gemma-7b-it"
    ]
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    for model in models_to_test:
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": "Hello"}],
            "max_tokens": 10
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers=headers,
                    json=payload
                )
                if response.status_code == 200:
                    print(f"WORKING: {model}")
                    return model  # Return first working model
                else:
                    print(f"FAILED: {model} - {response.status_code}: {response.text}")
        except Exception as e:
            print(f"ERROR: {model} - {str(e)}")
    
    return None

if __name__ == "__main__":
    import asyncio
    working_model = asyncio.run(test_groq_api())
    if working_model:
        print(f"\nUSE THIS MODEL: {working_model}")
    else:
        print("\nNO WORKING MODELS FOUND!")