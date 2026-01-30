# Nerua – AI Chat System

A production-ready, modular chat system built with **FastAPI**, **PostgreSQL**, **Docker**, and **Streamlit**. Nerua provides multi-user conversations with persistent chat history and a scalable architecture designed for AI-powered assistants.

---

## Features

- **UUID-based User Management** – Unique `user_id` for each user
- **Conversation Isolation** – Unique `chat_id` per conversation thread
- **Persistent Storage** – Chat history stored in PostgreSQL
- **Clean Architecture** – Modular CRUD operations and router-based API
- **Modern Frontend** – Interactive Streamlit interface
- **Containerized Database** – Docker-based PostgreSQL deployment
- **AI-Ready** – Prepared for LLM/AI integration

---

## Project Structure
```
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
│   └── streamlit_app.py
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | FastAPI, SQLAlchemy |
| Database | PostgreSQL |
| Frontend | Streamlit |
| Containerization | Docker Compose |
| Language | Python 3.12.12 |

---

## Getting Started

### Prerequisites

- Python 3.12+
- Docker & Docker Compose
- Git

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/<your-username>/nerua.git
cd nerua
```

**2. Create and activate virtual environment**
```bash
python -m venv chat
chat\Scripts\activate  # Windows
source chat/bin/activate  # macOS/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Start PostgreSQL database**
```bash
docker compose up -d
```

**5. Run the backend server**
```bash
cd backend
uvicorn app.main:app --reload
```

The API will be available at:
- **Application**: http://127.0.0.1:8000
- **API Documentation**: http://127.0.0.1:8000/docs

**6. Launch the frontend** (in a new terminal)
```bash
cd frontend
streamlit run streamlit_app.py
```

---

## Database Management

### Access PostgreSQL shell
```bash
docker exec -it nerua-db-1 psql -U nerua -d nerua_db
```

### Common commands
```sql
\dt                    -- List all tables
SELECT * FROM messages; -- View messages
\q                     -- Exit
```

---

## API Endpoints

Visit http://127.0.0.1:8000/docs for interactive API documentation.

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## License

This project is licensed under the MIT License.