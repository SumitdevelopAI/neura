from pydantic import BaseModel, Field
from datetime import datetime


# -------------------
# CHAT SCHEMAS
# -------------------

class ChatCreate(BaseModel):
    title: str


class ChatOut(ChatCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# -------------------
# MESSAGE SCHEMAS
# -------------------

class MessageCreate(BaseModel):
    user_id: str
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str


class MessageOut(MessageCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
