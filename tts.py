from gtts import gTTS
from pathlib import Path
import uuid

AUDIO_DIR = Path("audio")
AUDIO_DIR.mkdir(exist_ok=True)


def text_to_speech(text: str):
    filename = f"{uuid.uuid4()}.mp3"

    filepath = AUDIO_DIR / filename

    gTTS(
        text=text,
        lang="en",
        slow=False
    ).save(filepath)

    return filename
