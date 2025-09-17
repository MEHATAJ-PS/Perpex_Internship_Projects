import time


class SessionManager:
    def __init__(self, expiry_seconds: int):
        """
        Initialize the session manager.
        :param expiry_seconds: Number of seconds a session should remain active.
        """
        self.expiry_seconds = expiry_seconds
        self.sessions = {}  # {session_id: creation_time}

    def create_session(self, session_id: str):
        """
        Create a session for a given session_id.
        :param session_id: Unique identifier for the session.
        """
        self.sessions[session_id] = time.time()
        return f"Session {session_id} created."

    def is_session_active(self, session_id: str) -> bool:
        """
        Check if a session is active.
        :param session_id: Unique identifier for the session.
        :return: True if active, False otherwise.
        """
        if session_id not in self.sessions:
            return False

        creation_time = self.sessions[session_id]
        if time.time() - creation_time <= self.expiry_seconds:
            return True
        else:
            # Expired → delete automatically
            del self.sessions[session_id]
            return False

    def delete_session(self, session_id: str) -> str:
        """
        Delete a session manually.
        :param session_id: Unique identifier for the session.
        :return: "Deleted" if found, otherwise "Not Found".
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            return "Deleted"
        return "Not Found"


# ---------------------------
# Example Usage / Test Cases
# ---------------------------
if __name__ == "__main__":
    sm = SessionManager(expiry_seconds=3)

    print(sm.create_session("driver123"))  # Session created
    print(sm.is_session_active("driver123"))  # True

    time.sleep(2)
    print(sm.is_session_active("driver123"))  # Still True

    time.sleep(2)
    print(sm.is_session_active("driver123"))  # Expired → False

    print(sm.delete_session("driver123"))  # Already expired → "Not Found"

    sm.create_session("rider456")
    print(sm.delete_session("rider456"))  # "Deleted"
