from fastapi import FastAPI
from app.routers.chat import router as chat_router
from app.routers.documents import router as document_router
from app.routers.health import router as health_router

app = FastAPI(
    title="CortexFlow AI",
    version="0.1.0",
    description="Enterprise AI Workspace powered by LangGraph"
)

app.include_router(chat_router)
app.include_router(document_router)
app.include_router(health_router)