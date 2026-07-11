from google import genai
from google.genai import types

from config import Config
from memory import memory


client = genai.Client(api_key=Config.GEMINI_API_KEY)


SYSTEM_PROMPT = """
You are IRIS.

You are a premium desktop AI assistant.

Rules:

- Your name is IRIS.
- Never say you are Gemini.
- Never say you are Google AI.
- Never mention language models.
- Speak naturally.
- Keep replies concise.
- Be friendly.
- Be intelligent.
- If the user asks follow-up questions, use previous conversation context.
- Keep answers under 120 words unless the user explicitly requests more detail.
"""


def ask_gemini(user_message):

    memory.add_user(user_message)

    history = memory.get_history()

    conversation = SYSTEM_PROMPT + "\n\n"

    for item in history:

        if item["role"] == "user":
            conversation += f"User: {item['text']}\n"

        else:
            conversation += f"IRIS: {item['text']}\n"

    response = client.models.generate_content(
        model=Config.GEMINI_MODEL,
        contents=conversation,
        config=types.GenerateContentConfig(
            temperature=Config.TEMPERATURE,
            max_output_tokens=Config.MAX_RESPONSE_TOKENS,
        )
    )

    answer = response.text.strip()

    memory.add_assistant(answer)

    return answer
