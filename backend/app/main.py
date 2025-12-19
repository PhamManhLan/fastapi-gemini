from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth import router as auth_router
from app.routers.chat import router as chat_router
from app.database.db import Base, engine
from app.core.vector_db import load_knowledge_if_empty
from app.models.chat_history import ChatHistory

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Hướng Dẫn Viên Du Lịch Huế",
    description="Chatbot AI hỗ trợ du lịch Huế với RAG",
    version="1.0.0"
)

# CORS cho frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(chat_router)

# Load data vào Chroma khi server khởi động
@app.on_event("startup")
async def startup_event():
    load_knowledge_if_empty()
    print("Đã tải kiến thức du lịch Huế vào Vector DB!")

# Route gốc
@app.get("/")
async def root():
    return {"message": "Chào mừng đến với API Hướng Dẫn Viên Du Lịch Huế!"}