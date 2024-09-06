#!/usr/bin/env python3
"""
SessionAuth module
"""
from uuid import uuid4
from api.v1.auth.auth import Auth
# from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user import User
from typing import Optional, Type


class SessionAuth(Auth):
    """
    SessionAuth class for handling session-based authentication
    """

    # Class attribute to store user ID by session ID
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a session ID for a given user_id.

        Args:
            user_id (str): The ID of the user to create a session for.

        Returns:
            str: The session ID if created successfully, otherwise None.
        """
        # Return None if user_id is None or not a string
        if user_id is None or not isinstance(user_id, str):
            return None

        # Generate a new session ID using uuid4
        session_id = str(uuid4())

        # Store the session ID with the corresponding user_id
        self.user_id_by_session_id[session_id] = user_id

        # Return the created session ID
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves a User ID based on a Session ID.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            str: The User ID associated with the
            session ID, or None if not found.
        """
        # Return None if session_id is None or not a string
        if session_id is None or not isinstance(session_id, str):
            return None

        # Return the user_id associated with the session_id
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> Optional[Type['User']]:
        """
        Retrieves the current user based on the request.

        Args:
            request: The Flask request object.

        Returns:
            Optional[Type['User']]: The User instance, or None if not found.
        """
        # Get the session ID from the request
        session_id = self.session_cookie(request)

        # Get the user ID associated with the session ID
        user_id = self.user_id_for_session_id(session_id)

        # Return the User instance based on the user ID
        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        Deletes the user session/logout.
        """
        # Check if the request is None
        if request is None:
            return False

        # Retrieve the session ID from the cookie in the request
        session_id = self.session_cookie(request)

        # If the session ID is not found in the request cookies, return False
        if session_id is None:
            return False

        # Retrieve the user ID associated with the session ID
        user_id = self.user_id_for_session_id(session_id)

        # If no user ID is associated with the session ID, return False
        if user_id is None:
            return False

        # Delete the session ID from the session dictionary
        del self.user_id_by_session_id[session_id]

        return True
