from fastapi import APIRouter
from pydantic import BaseModel

from gemini_service import ask_gemini

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
async def chat(request: ChatRequest):

    reply = ask_gemini(request.message)

    return {
        "success": True,
        "reply": reply
    }
