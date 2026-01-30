from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas import MessageCreate, MessageOut
from crud.message import create_message, get_messages
from crud.chat import get_chat

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.post("/{chat_id}", response_model=MessageOut)
def add(chat_id: int, payload: MessageCreate, db: Session = Depends(get_db)):
    if not get_chat(db, chat_id):
        raise HTTPException(404, "Chat not found")

    return create_message(
        db,
        chat_id,
        payload.user_id,
        payload.role,
        payload.content
    )


@router.get("/{chat_id}/{user_id}", response_model=list[MessageOut])
def read(chat_id: int, user_id: str, db: Session = Depends(get_db)):
    return get_messages(db, chat_id, user_id)