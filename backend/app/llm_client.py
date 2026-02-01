import requests
from typing import List, Dict

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"

def generate_reply(messages: List[Dict[str, str]]) -> str:
    """
    messages = [
        {"role": "user", "content": "..."},
        {"role": "assistant", "content": "..."}
    ]
    """

    prompt = ""
    for m in messages:
        prompt += f"{m['role'].upper()}: {m['content']}\n"
    prompt += "ASSISTANT:"

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_ctx": 2048,      # ⚡ faster than 8k
                "num_predict": 256    # ⚡ limit output
            }
        },
        timeout=120
    )

    response.raise_for_status()
    return response.json()["response"]
