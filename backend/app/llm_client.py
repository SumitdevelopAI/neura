import requests
import json

# SWITCH TO CHAT ENDPOINT
# /api/chat is required for Llama 3 to understand conversation history correctly.
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3"

# Reuse the connection to speed up consecutive messages
session = requests.Session()

def generate_reply(messages: list[dict]) -> str:
    """
    Optimized for RTX 3050 (4GB VRAM).
    
    Args:
        messages: A list of message dictionaries.
                  Example: 
                  [
                      {"role": "user", "content": "Hello"}, 
                      {"role": "assistant", "content": "Hi there!"}
                  ]
    """
    
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False,
        "keep_alive": "10m",  # Keep model in memory for 10 mins (faster follow-ups)
        
        "options": {
            # --- HARDWARE OPTIMIZATION FOR 4GB VRAM ---
            # Default is 4096. Lowering to 2048 saves ~500MB VRAM.
            # This allows more of the model layers to run on your GPU 
            # instead of your slower CPU RAM.
            "num_ctx": 2048,
            
            # --- RESPONSE CONTROL ---
            # Stop generating after ~300 words to prevent freezing
            "num_predict": 400,
            
            # Creativity settings
            "temperature": 0.7,
            "top_p": 0.9,
        }
    }

    try:
        # Increased timeout to 120s because 4GB VRAM might be slightly slower
        response = session.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        
        # The /api/chat endpoint returns data in 'message' -> 'content'
        return response.json()["message"]["content"]

    except requests.exceptions.ConnectionError:
        print("Error: Ollama is not accessible.")
        return "Error: Could not connect to local AI server. Is Ollama running?"
    except Exception as e:
        print(f"Error generation: {e}")
        return f"Error: {str(e)}"