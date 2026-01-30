from sqlalchemy.orm import Session
from app.models import Chat


def create_chat(db: Session, title: str):
    chat = Chat(title=title)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat


def get_chat(db: Session, chat_id: int):
    return db.query(Chat).filter(Chat.id == chat_id).first()


def delete_chat(db: Session, chat_id: int):
    chat = get_chat(db, chat_id)
    if not chat:
        return None
    db.delete(chat)
    db.commit()
    return chat
