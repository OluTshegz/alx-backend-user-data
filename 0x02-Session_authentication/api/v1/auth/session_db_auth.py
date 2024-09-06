#!/usr/bin/env python3
"""
SessionDBAuth class module
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class for session management with database storage
    """

    def create_session(self, user_id=None):
        """
        Create a session and store it in the database
        """
        if user_id is None:
            return None
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieve the user ID for a session ID by querying the database
        """
        if session_id is None:
            return None

        UserSession.load_from_file()
        sessions = UserSession.search({'session_id': session_id})
        if not sessions:
            return None

        user_session = sessions[0]

        if self.session_duration <= 0:
            return user_session.user_id

        if user_session.created_at is None:
            return None

        expiration_time = user_session.created_at + \
            timedelta(seconds=self.session_duration)
        if expiration_time < datetime.now():
            return None

        return user_session.user_id

    def destroy_session(self, request=None):
        """
        Destroy a session by deleting it from the database
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        if not self.user_id_for_session_id(session_id):
            return False

        UserSession.load_from_file()
        sessions = UserSession.search({'session_id': session_id})
        if not sessions:
            return False

        user_session = sessions[0]
        try:
            user_session.remove()
            UserSession.save_to_file()
        except Exception:
            return False

        return True
