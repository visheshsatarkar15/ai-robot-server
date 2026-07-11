from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from auth import verify_device
from gemini_service import ask_gemini
from tts import text_to_speech

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


# --------------------------------------------------
# TEXT ENDPOINT (Used for testing)
# --------------------------------------------------

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


# --------------------------------------------------
# SPEECH ENDPOINT (Used by IRIS Robot)
# --------------------------------------------------

@router.post("/speak")
async def speak(
    request: ChatRequest,
    _: None = Depends(verify_device)
):
    reply = ask_gemini(request.message)

    audio = text_to_speech(reply)

    return StreamingResponse(
        audio,
        media_type="audio/mpeg"
    )
