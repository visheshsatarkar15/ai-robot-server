from collections import deque
from config import Config


class IrisMemory:

    def __init__(self):

        # Conversation History
        self.history = deque(maxlen=Config.MAX_HISTORY)

        # Session Information
        self.user_name = None
        self.last_topic = None
        self.last_question = None

        # Robot Status
        self.robot_state = "idle"

    # ----------------------------
    # Conversation
    # ----------------------------

    def add_user(self, text):

        self.last_question = text

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

    def clear_history(self):
        self.history.clear()

    # ----------------------------
    # User
    # ----------------------------

    def set_user_name(self, name):
        self.user_name = name

    def get_user_name(self):
        return self.user_name

    # ----------------------------
    # Topics
    # ----------------------------

    def set_last_topic(self, topic):
        self.last_topic = topic

    def get_last_topic(self):
        return self.last_topic

    # ----------------------------
    # Robot State
    # ----------------------------

    def set_robot_state(self, state):
        self.robot_state = state

    def get_robot_state(self):
        return self.robot_state


memory = IrisMemory()
