import requests

API = "http://127.0.0.1:8000"


def create_chat(title: str):
    r = requests.post(f"{API}/chats/", json={"title": title})
    r.raise_for_status()
    return r.json()


def get_messages(chat_id: int, user_id: str):
    r = requests.get(f"{API}/messages/{chat_id}/{user_id}")
    r.raise_for_status()
    return r.json()


def send_message(chat_id: int, user_id: str, content: str):
    r = requests.post(
        f"{API}/messages/{chat_id}",
        json={
            "user_id": user_id,
            "role": "user",
            "content": content
        }
    )
    r.raise_for_status()
    return r.json()
