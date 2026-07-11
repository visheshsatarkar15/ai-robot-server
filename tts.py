from gtts import gTTS
from io import BytesIO


def text_to_speech(text: str):
    tts = gTTS(
        text=text,
        lang="en",
        slow=False
    )

    audio = BytesIO()

    tts.write_to_fp(audio)

    audio.seek(0)

    return audio
