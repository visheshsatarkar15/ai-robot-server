from fastapi import FastAPI
import os
from google import genai

app = FastAPI(title="IRIS Server v1.0")

client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)

@app.get("/")
def root():
    return {
        "status": "online",
        "name": "IRIS Server v1.0",
        "message": "IRIS Cloud Brain is running."
    }
