from fastapi import FastAPI
from app.db import engine, Base
from routers import chat, message

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Nerua Backend")

app.include_router(chat.router)
app.include_router(message.router)
