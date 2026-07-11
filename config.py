import os

# ==============================
# IRIS SERVER CONFIGURATION
# ==============================

class Config:

    # Robot Name
    ROBOT_NAME = "IRIS"

    # Gemini API Key
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # Gemini Model
    GEMINI_MODEL = "gemini-2.5-flash"

    # Conversation Memory
    MAX_HISTORY = 10

    # Maximum response length
    MAX_RESPONSE_TOKENS = 200

    # Temperature
    TEMPERATURE = 0.7

    # Audio Settings
    SAMPLE_RATE = 16000

    CHANNELS = 1

    AUDIO_FORMAT = "wav"
