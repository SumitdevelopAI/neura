from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ChatBase(BaseModel):
    title: str

class ChatCreate(ChatBase):
    pass

class ChatOut(ChatBase):
    id: int
    created_at: datetime
    # This allows the schema to read data from SQLAlchemy models
    class Config:
        from_attributes = True

class MessageCreate(BaseModel):
    user_id: str
    role: str
    content: str

class MessageOut(BaseModel):
    id: int
    chat_id: int
    user_id: str
    role: str
    content: str
    timestamp: Optional[datetime] = None

    class Config:
        from_attributes = True