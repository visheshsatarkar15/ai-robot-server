from collections import deque

from config import Config


class ConversationMemory:

    def __init__(self):
        self.history = deque(maxlen=Config.MAX_HISTORY)

    def add_user(self, text):
        self.history.append({
            "role": "user",
            "text": text
        })

    def add_assistant(self, text):
        self.history.append({
            "role": "assistant",
            "text": text
        })

    def get_history(self):
        return list(self.history)

    def clear(self):
        self.history.clear()


memory = ConversationMemory()
