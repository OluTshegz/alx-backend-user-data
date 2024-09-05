#!/usr/bin/env python3
""" Module of Basic Authentication
"""

from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
import base64
# from typing import Optional


class BasicAuth(Auth):
    """BasicAuth class that inherits from Auth
    and implements basic authentication."""

    # def extract_base64_authorization_header(self, author
    # ization_header: Optional[str]) -> Optional[str]:
    def extract_base64_authorization_header(self, authorization_header:
                                            str) -> str:
        """
        Extracts the Base64 part from the
        Authorization header for Basic Authentication.

        Args:
            authorization_header (str): The Authorization
            header from the request.

        Returns:
            str: The Base64 part of the Authorization header,
            or None if invalid.
        """
        # Return None if authorization_header is None
        if authorization_header is None:
            return None

        # Return None if authorization_header is not a string
        if not isinstance(authorization_header, str):
            return None

        # Check if authorization_header starts with
        # "Basic " (with a space at the end)
        if not authorization_header.startswith("Basic "):
            return None

        # Return the part of the string after "Basic "
        return authorization_header[len("Basic "):]

    # def decode_base64_authorization_header(self, base64_author
    # ization_header: Optional[str]) -> Optional[str]:
    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """
        Decodes a Base64 string to its original form.

        Args:
            base64_authorization_header (str): The Base64 string to decode.

        Returns:
            str: The decoded string, or None if decoding fails.
        """
        # Return None if base64_authorization_header is None
        if base64_authorization_header is None:
            return None

        # Return None if base64_authorization_header is not a string
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            encoded_bytes = base64_authorization_header.encode('utf-8')
            # Attempt to decode the Base64 string
            decoded_bytes = base64.b64decode(encoded_bytes)
            # Return the decoded string in UTF-8 format
            return decoded_bytes.decode('utf-8')
        except Exception:
            # Return None if decoding fails
            return None

    # def extract_user_credentials(self, decoded_base64_authorization_header:
    # Optional[str]) -> Optional[Tuple[str, str]]:
    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """
        Extracts user email and password from the Base64 decoded
        authorization header, allowing for colons in the password.

        Args:
            decoded_base64_authorization_header (str):
            Decoded Base64 string of the format "email:password".

        Returns:
            Tuple (str, str): A tuple containing user
            email and password, or (None, None) if invalid.
        """
        # Return (None, None) if decoded_base64_authorization_header
        # is None
        if decoded_base64_authorization_header is None:
            return None, None

        # Return (None, None) if decoded_base64_authorization_header
        # is not a string
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        # Return (None, None) if decoded_base64_authorization_header
        # doesn't contain ':'
        if ':' not in decoded_base64_authorization_header:
            return None, None

        # Split the string at the first ':' to get
        # email and the rest as the password
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    # def user_object_from_credentials(self, user_email:
    #                                  str, user_pwd: str) -> User:
    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        Returns the User instance based on the email and password provided.

        Args:
            user_email (str): The user's email address.
            user_pwd (str): The user's password.

        Returns:
            User: The User instance if authentication is successful,
            or None if any validation fails.
        """
        # Return None if user_email is None or not a string
        if user_email is None or not isinstance(user_email, str):
            return None

        # Return None if user_pwd is None or not a string
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            # Search for the user by email
            users = User.search({'email': user_email})

            # Return None if no user found with the given email
            if not users or users == []:
                return None

            # user = users[0]
            for user in users:
                # Validate the password using the
                # User's is_valid_password method
                if not user.is_valid_password(user_pwd):
                    return None
                # Return the User instance if authentication is successful
                return user
        except Exception:
            return None

    # def current_user(self, request=None) -> Optional[TypeVar('User')]:
    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the User instance for a
        request using Basic Authentication.

        Args:
            request: The HTTP request object.

        Returns:
            User: The User instance if authentication
            is successful, or None if not.
        """
        # Retrieve the Authorization header
        auth_header = self.authorization_header(request)
        if auth_header is not None:
            # Extract the Base64 part from the header
            b64_token = self.extract_base64_authorization_header(auth_header)
            if b64_token is not None:
                # Decode the Base64 value
                decoded = self.decode_base64_authorization_header(b64_token)
                if decoded is not None:
                    # Extract the user credentials (email and password)
                    email, password = self.extract_user_credentials(decoded)
                    if email is not None:
                        # Retrieve and return the User object
                        return self.user_object_from_credentials(email,
                                                                 password)

        # Return None if any step fails
        return None  # or just return or pass, do nothing
