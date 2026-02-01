from sqlalchemy.orm import Session
from app.models import Message


def create_message(
    db: Session,
    chat_id: int,
    user_id: str,
    role: str,
    content: str
):
    msg = Message(
        chat_id=chat_id,
        user_id=user_id,
        role=role,
        content=content
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


def get_messages(db: Session, chat_id: int, user_id: str):
    return (
        db.query(Message)
        .filter(
            Message.chat_id == chat_id,
            Message.user_id == user_id
        )
        .order_by(Message.created_at.asc())
        .all()
    )
