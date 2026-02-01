from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas import MessageCreate, MessageOut
from crud.chat import get_chat
from crud.message import create_message, get_messages
from app.llm_client import generate_reply

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.post("/{chat_id}", response_model=MessageOut)
def add_message(chat_id: int, payload: MessageCreate, db: Session = Depends(get_db)):
    chat = get_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    # 1️⃣ Save user message
    create_message(
        db,
        chat_id,
        payload.user_id,
        "user",
        payload.content
    )

    # 2️⃣ Get full history
    history = get_messages(db, chat_id, payload.user_id)

    formatted = [
        {"role": m.role, "content": m.content}
        for m in history
    ]

    # 3️⃣ Call LLM
    reply = generate_reply(formatted)

    # 4️⃣ Save assistant message
    assistant_msg = create_message(
        db,
        chat_id,
        payload.user_id,
        "assistant",
        reply
    )

    return assistant_msg


@router.get("/{chat_id}/{user_id}", response_model=list[MessageOut])
def read_messages(chat_id: int, user_id: str, db: Session = Depends(get_db)):
    return get_messages(db, chat_id, user_id)
