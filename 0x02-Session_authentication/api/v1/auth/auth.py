#!/usr/bin/env python3
""" Module of Authentication
"""
from flask import request
# from models.user import User
import os
from typing import List, TypeVar
# from typing import Optional, Type


class Auth:
    """Auth class for managing the API authentication."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if the path requires authentication.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): A list of paths
            that are excluded from authentication.

        Returns:
            bool: True if the path is not in excluded_paths, otherwise False.
        """
        # If path is None, return True (path requires authentication)
        # if path is None or path == '' or not path:
        #     return True

        # If excluded_paths is None or empty,
        # return True (path requires authentication)
        # if excluded_paths is None or excluded_paths == []:
        #     return True

        # if not excluded_paths:
        #     return True

        # Normalize path by ensuring it ends with a '/'
        # if path[-1] != '/':
        # if not path.endswith('/'):
        #     path += '/'

        # Normalize all paths in excluded_paths
        # by ensuring they end with a '/'
        # excluded_paths = [p + '/' if not p.endswith('/')
        #                  else p for p in excluded_paths]

        # Create an empty list to store the modified paths
        # modified_paths = []

        # Iterate over each path in the original excluded_paths list
        # for p in excluded_paths:
        #     Check if the path does not end with a '/'
        #     if not p.endswith('/'):
        #         If it doesn't, add '/' to the end of the path
        #         and append to modified_paths
        #         modified_paths.append(p + '/')
        #     else:
        #         If it already ends with '/',
        #         just append it as is to modified_paths
        #         modified_paths.append(p)

        # Now, modified_paths contains the paths with the proper format
        # excluded_paths = modified_paths

        # Check if path starts with any excluded path or vice versa
        # for excluded_path in excluded_paths:
        #     if excluded_path.startswith(path):
        #         return False

        #     if path.startswith(excluded_path):
        #         return False

        #     Handle wildcard paths
        #     if excluded_path.endswith("*"):
        #         if path.startswith(excluded_path[:-1]):
        #             return False

        # Check if the normalized path is in the list of excluded paths
        # if path in excluded_paths:
        #     return False

        # If the path is not in excluded paths, it requires authentication
        # return True

        if path is None:
            return True

        # Ensure path ends with '/' for consistency
        if not path.endswith('/'):
            path += '/'

        # Normalize excluded paths to ensure they end with '/'
        excluded_paths = [
            p if p.endswith('/') else p + '/' for p in excluded_paths
        ]

        # Check if the path matches any excluded path
        if path in excluded_paths:
            return False

        # Handle wildcard paths (e.g., /api/v1/stat*)
        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False

        return True

    # def authorization_header(self, request:
    #                         Optional[str] = None) -> Optional[str]:
    def authorization_header(self, request=None) -> str:
        """
        Retrieves the Authorization header from the request.

        Args:
            request: The Flask request object.

        Returns:
            str: None, as this is a template method.
        """
        if request is None:
            return None

        auth_header = request.headers.get('Authorization')

        if auth_header is None:
            return None

        return auth_header

    # def current_user(self, request:
    #                 Optional[str] = None) -> Optional[Type['User']]:
    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user based on the request.

        Args:
            request: The Flask request object.

        Returns:
            Optional[Type['User']]: None, as this is a template method.
        """
        return None

    def session_cookie(self, request=None):
        """
        Retrieves the session cookie from the request.

        Args:
            request: The Flask request object.

        Returns:
            str: None, as this is a template method.
        """
        # Return None if the request is None
        if request is None:
            return None

        # Get the session cookie name from the
        # environment variable SESSION_NAME
        session_name = os.getenv('SESSION_NAME')

        if session_name is None:
            return None

        session_cookie = request.cookies.get(session_name)

        if session_cookie is None:
            return None

        # Return the cookie value associated with the session_name
        return session_cookie
