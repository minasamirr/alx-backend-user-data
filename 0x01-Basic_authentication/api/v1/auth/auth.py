#!/usr/bin/env python3
"""Authentication module for the API.
"""
import re
from typing import List, TypeVar
from flask import request


class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Determines if authentication is required """
        return False

    def authorization_header(self, request=None) -> str:
        """ Returns the authorization header from the request """
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns the current user """
        return None
