from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import Depends
from auth import verify_device

from gemini_service import ask_gemini

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
async def chat(
    request: ChatRequest,
    _: None = Depends(verify_device)
):

    reply = ask_gemini(request.message)

    return {
        "success": True,
        "reply": reply
    }
