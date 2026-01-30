from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas import ChatCreate, ChatOut
from crud.chat import create_chat, get_chat

router = APIRouter(prefix="/chats", tags=["Chats"])


@router.post("/", response_model=ChatOut)
def create(payload: ChatCreate, db: Session = Depends(get_db)):
    return create_chat(db, payload.title)


@router.get("/{chat_id}", response_model=ChatOut)
def read(chat_id: int, db: Session = Depends(get_db)):
    chat = get_chat(db, chat_id)
    if not chat:
        raise HTTPException(404, "Chat not found")
    return chat
