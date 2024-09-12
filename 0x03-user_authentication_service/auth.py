#!/usr/bin/env python3
"""
Auth module for handling authentication
"""
from db import DB
from user import User
import bcrypt
from sqlalchemy.exc import NoResultFound
from typing import Optional
import uuid


def _hash_password(password: str) -> bytes:
    """Hash a password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted hash of the password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate a new UUID."""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        # Private DB instance
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user with an email and password.

        Args:
            email (str): The user's email.
            password (str): The user's password.

        Returns:
            User: The newly registered user.

        Raises:
            ValueError: If the user already exists.
        """
        try:
            self._db.find_user_by(email=email)
            # Raise if user already exists
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # Hash the password
            hashed_password = _hash_password(password)
            # Return the added user
            return self._db.add_user(email, hashed_password.decode('utf-8'))

    def valid_login(self, email: str, password: str) -> bool:
        """Validate user login credentials."""
        try:
            # Find user by email
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password.encode('utf-8'))
        except NoResultFound:
            # Return False if user is not found
            return False

    def create_session(self, email: str) -> str:
        """Create a session for a user and return the session ID."""
        try:
            # Find user by email
            user = self._db.find_user_by(email=email)
            # Generate a session ID
            session_id = _generate_uuid()
            # Set the session ID for the user
            user.session_id = session_id
            # Commit the session to persist the session ID
            self._db._session.commit()
            # Return the session ID
            return session_id
        except NoResultFound:
            # Return None if no user is found
            return None

    def get_user_from_session_id(self, session_id:
                                 Optional[str]) -> Optional[User]:
        """
        Retrieves the user based on session_id.
        Returns the user or None if not found or session_id is None.
        """
        if session_id is None:
            return None

        # Use DB to find the user by session_id
        return self._db.find_user_by(session_id=session_id)

    def destroy_session(self, user_id: int) -> None:
        """
        Invalidate the user's session by setting the session_id to None.
        """
        # Find user by user_id
        user = self._db.find_user_by(id=user_id)
        if user:
            # Set session_id to None
            self._db.update_user(user.id, session_id=None)
