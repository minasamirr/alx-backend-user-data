#!/usr/bin/env python3
""" Auth module
"""
from typing import List, TypeVar
from flask import request

User = TypeVar('User')


class Auth:
    """ Auth class to manage API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Determine if authentication is required for the given path

        Args:
            path (str): The request path
            excluded_paths (List[str]): List of paths that do not require
            authentication

        Returns:
            bool: True if authentication is required, False otherwise
        """
        # If path is None, authentication is required
        if path is None:
            return True

        # If excluded_paths is None or empty, authentication is required
        if excluded_paths is None or not excluded_paths:
            return True

        # Normalize the path
        normalized_path = path if path.endswith('/') else path + '/'

        # Check if the path is in the excluded_paths
        for excluded_path in excluded_paths:
            if (normalized_path == excluded_path or
                normalized_path.startswith(excluded_path)):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Get the authorization header from the request

        Args:
            request: The Flask request object

        Returns:
            str: The authorization header value or None if not present
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> User:
        """ Get the current user from the request

        Args:
            request: The Flask request object

        Returns:
            User: The current user or None if not authenticated
        """
        return None
