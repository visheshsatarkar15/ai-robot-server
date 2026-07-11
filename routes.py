from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from pydantic import BaseModel

from auth import verify_device
from gemini_service import ask_gemini
from tts import text_to_speech

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


@router.post("/speak")
async def speak(
    request: ChatRequest,
    _: None = Depends(verify_device)
):
    reply = ask_gemini(request.message)

    filename = text_to_speech(reply)

    return {
        "success": True,
        "reply": reply,
        "audio_url": f"/audio/{filename}"
    }


@router.get("/audio/{filename}")
async def get_audio(filename: str):

    return FileResponse(
        f"audio/{filename}",
        media_type="audio/mpeg"
    )
