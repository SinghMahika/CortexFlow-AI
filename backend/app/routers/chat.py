from unittest import result

from fastapi import APIRouter
from httpx import request
from app.models.chat import ChatRequest, ChatResponse
from app.core.workflow import run_workflow

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):

    result = run_workflow(request.message)

    return ChatResponse(
        response=result["response"],
        sources=result.get("sources", []),
        intent=result.get("intent"),
        generated_sql=result.get("generated_sql"),
    )