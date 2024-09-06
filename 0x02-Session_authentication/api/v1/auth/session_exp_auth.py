#!/usr/bin/env python3
"""
SessionExpAuth class module
"""
from datetime import datetime, timedelta
from os import getenv
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth class that adds session expiration functionality
    """

    def __init__(self):
        """
        Initialize the SessionExpAuth instance
        """
        # super().__init__()
        # Set session_duration from environment
        # variable or default to 0 if invalid
        try:
            session_duration = int(getenv('SESSION_DURATION', '0'))
        except Exception:
            session_duration = 0
        self.session_duration = session_duration

    def create_session(self, user_id=None):
        """
        Create a new session with an expiration date
        """
        if user_id is None:
            return None
        # Generate session ID using the parent method
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        # Store the session information with creation time
        session_dict = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        SessionAuth.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Return the user_id associated with the
        session_id if the session has not expired
        """
        if session_id is None:
            return None

        if session_id not in SessionAuth.user_id_by_session_id.keys():
            return None

        # Retrieve the session dictionary using the session ID
        session_dict = SessionAuth.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None

        if self.session_duration <= 0:
            # If no expiration is set, return the user_id
            return session_dict.get("user_id")

        if "created_at" not in session_dict.keys():
            return None

        # Calculate session expiration time
        created_at = session_dict.get("created_at")
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if expiration_time < datetime.now():
            # If the session has expired, return None
            return None

        return session_dict.get("user_id")
