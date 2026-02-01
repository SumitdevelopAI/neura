# Nerua – AI Chat System

A production-ready, modular AI chat system built with FastAPI, PostgreSQL, Docker, and Streamlit. Nerua supports multi-user conversations, persistent chat history, and local LLM inference using Ollama (llama3) with GPU acceleration.

**Repository:** https://github.com/SumitdevelopAI/neura

---

## Technology Stack

![Python](https://img.shields.io/badge/Python-3.12.10-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.12-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-27.4.1-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.41.1-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.36-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-llama3-000000?style=for-the-badge&logo=ollama&logoColor=white)
![CUDA](https://img.shields.io/badge/CUDA-Enabled-76B900?style=for-the-badge&logo=nvidia&logoColor=white)

| Component   | Technology             | Version  |
|-------------|------------------------|----------|
| Language    | Python                 | 3.12.10  |
| Backend     | FastAPI                | 0.115.12 |
| ORM         | SQLAlchemy             | 2.0.36   |
| Database    | PostgreSQL             | 17       |
| Frontend    | Streamlit              | 1.41.1   |
| Container   | Docker Compose         | 27.4.1   |
| Local LLM   | Ollama (llama3)        | Latest   |
| GPU Support | NVIDIA CUDA            | Verified |
| HTTP Client | httpx                  | 0.28.1   |
| ASGI Server | uvicorn                | 0.34.0   |

---

## Features

- UUID-based lightweight user identity (per browser session)
- One `chat_id` per conversation thread
- Persistent message storage in PostgreSQL
- Clean backend architecture (`crud`, `routers`, `schemas`)
- Streamlit frontend for rapid interaction
- Local LLM inference via Ollama (`llama3`)
- GPU acceleration supported and verified

---

## Project Structure

```text
Nerua/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── db.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── llm_client.py
│   ├── crud/
│   │   ├── chat.py
│   │   └── message.py
│   └── routers/
│       ├── chat.py
│       └── message.py
├── frontend/
│   ├── api.py
│   └── streamlit_app.py
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.12.10
- Docker and Docker Compose
- Ollama installed locally
- NVIDIA GPU with CUDA support (optional, for acceleration)

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/SumitdevelopAI/neura.git
cd neura
```

#### 2. Create and Activate Virtual Environment

**Windows:**
```bash
python -m venv chat
chat\Scripts\activate
```

**macOS / Linux:**
```bash
python -m venv chat
source chat/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Start PostgreSQL Database

```bash
docker compose up -d
docker ps
```

Ensure the container `nerua-db-1` is running.

#### 5. Start Ollama (Local LLM)

```bash
ollama serve
```

In a new terminal, pull and verify the model:

```bash
ollama pull llama3
ollama list
ollama ps
```

#### 6. Start Backend (FastAPI)

```bash
cd backend
uvicorn app.main:app --reload
```

Access the application:
- API: http://127.0.0.1:8000
- API Documentation: http://127.0.0.1:8000/docs

#### 7. Start Frontend (Streamlit)

Open a new terminal:

```bash
cd frontend
streamlit run streamlit_app.py
```

---

## How It Works

1. Streamlit generates a unique `user_id` per session
2. A new conversation creates a `chat_id`
3. User messages are sent to the backend
4. Backend processes the request:
   - Stores user message
   - Fetches recent chat context
   - Calls Ollama (llama3)
   - Stores assistant reply
5. Frontend fetches updated history and renders messages

---

## API Usage

### Create Chat

```bash
curl -X POST http://127.0.0.1:8000/chats/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Chat"}'
```

### Send Message

```bash
curl -X POST http://127.0.0.1:8000/messages/1 \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test-user",
    "role": "user",
    "content": "Hello"
  }'
```

### Fetch Chat Messages

```bash
curl http://127.0.0.1:8000/messages/1/test-user
```

---

## Database Access

Enter PostgreSQL shell:

```bash
docker exec -it nerua-db-1 psql -U nerua -d nerua_db
```

Useful commands:

```sql
\dt
SELECT * FROM messages ORDER BY created_at;
\q
```

---

## Troubleshooting

### Ollama not responding

- Ensure `ollama serve` is running
- Check port 11434 is accessible
- Verify with: `curl http://localhost:11434/api/generate`

### Slow responses

- First request warms up the model
- Keep model hot: `ollama run llama3 "ping"`
- Limit context size for faster replies

### Streamlit shows no AI reply

- Confirm backend returned `role: assistant`
- Verify database entries for assistant messages

---

## Git Workflow

```bash
git add .
git commit -m "feat: implement feature description"
git pull origin main
git push origin main
```

---

## Future Improvements

- Streaming token responses
- Context summarization
- Authentication (JWT / OAuth)
- Multi-model support
- Full Dockerized stack
- Performance and GPU metrics

---

## License

This project is licensed under the MIT License.

---

## Contributing

Contributions are welcome. Please open an issue or submit a pull request for any improvements.
