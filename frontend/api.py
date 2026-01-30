import requests

API_BASE_URL = "http://127.0.0.1:8000"

def create_chat(title: str):
    response = requests.post(
        f"{API_BASE_URL}/chats",
        json={"title": title}
    )
    response.raise_for_status()
    return response.json()

def get_chat(chat_id: int):
    response = requests.get(
        f"{API_BASE_URL}/chats/{chat_id}"
    )
    response.raise_for_status()
    return response.json()
