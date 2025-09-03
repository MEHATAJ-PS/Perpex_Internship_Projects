# task5_Session_Expiry_System.py
import time
import uuid


class SessionManager:
    def __init__(self, session_lifetime):
        """
        Initialize the SessionManager.
        :param session_lifetime: Session lifetime in seconds.
        """
        self.session_lifetime = session_lifetime
        self.sessions = {}  # {session_id: expiry_time}

    def create_session(self, user_id):
        """
        Create a new session for a user.
        :param user_id: Unique identifier for the user.
        :return: session_id
        """
        session_id = str(uuid.uuid4())  # Generate unique session ID
        expiry_time = time.time() + self.session_lifetime
        self.sessions[session_id] = {"user_id": user_id, "expiry": expiry_time}
        return session_id

    def is_session_active(self, session_id):
        """
        Check if the session is still active.
        Expired sessions are automatically removed.
        :param session_id: The session ID to validate.
        :return: True if active, False if expired or not found.
        """
        self.remove_expired_sessions()

        if session_id in self.sessions:
            return True
        return False

    def remove_expired_sessions(self):
        """
        Remove sessions that have passed their expiry time.
        """
        current_time = time.time()
        expired_keys = [
            sid for sid, data in self.sessions.items()
            if current_time > data["expiry"]
        ]
        for sid in expired_keys:
            del self.sessions[sid]


if __name__ == "__main__":
    # Example usage
    session_manager = SessionManager(session_lifetime=10)  # 10 seconds lifetime
    user_id = "user_123"

    print("\nCreating a session...")
    session_id = session_manager.create_session(user_id)
    print(f"Session ID: {session_id}")

    print("\nChecking session immediately:")
    print("Active:", session_manager.is_session_active(session_id))

    print("\nWaiting 12 seconds for expiry...")
    time.sleep(12)

    print("\nChecking session after expiry:")
    print("Active:", session_manager.is_session_active(session_id))
