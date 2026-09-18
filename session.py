import uuid
from datetime import datetime


class RudraSession:

    def __init__(self):
        self.session_id = str(uuid.uuid4())[:8].upper()
        self.started_at = datetime.now()
        self.message_count = 0
        self.active = True

    def register_message(self):
        self.message_count += 1

    def status(self):
        return {
            "session_id": self.session_id,
            "started_at": self.started_at.strftime(
                "%d %B %Y, %I:%M:%S %p"
            ),
            "messages": self.message_count,
            "status": "ACTIVE" if self.active else "CLOSED"
        }

    def close(self):
        self.active = False