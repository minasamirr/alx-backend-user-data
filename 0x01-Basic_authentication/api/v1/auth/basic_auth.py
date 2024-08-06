#!/usr/bin/env python3
""" BasicAuth module
"""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """ BasicAuth class for basic authentication """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Extracts the Base64 part of the Authorization header for Basic
        Authentication

        Args:
            authorization_header (str): The Authorization header

        Returns:
            str: The Base64 part of the header, or None if the header is
            invalid
        """
        if authorization_header is None or not isinstance(
                authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Decodes the Base64 part of the Authorization header

        Args:
            base64_authorization_header (str): The Base64 encoded part of
            the Authorization header

        Returns:
            str: The decoded value as UTF8 string, or None if the input is
            invalid
        """
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ Extracts user email and password from the Base64 decoded value

        Args:
            decoded_base64_authorization_header (str): The Base64 decoded value

        Returns:
            tuple: The user email and password, or (None, None) if invalid
        """
        if decoded_base64_authorization_header is None or not isinstance(
                decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        user_credentials = decoded_base64_authorization_header.split(':', 1)
        return user_credentials[0], user_credentials[1]

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> User:
        """ Returns the User instance based on his email and password

        Args:
            user_email (str): The user's email
            user_pwd (str): The user's password

        Returns:
            User: The User instance or None if credentials are invalid
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        user_list = User.search({"email": user_email})
        if not user_list:
            return None
        user = user_list[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> User:
        """ Retrieves the User instance for a request

        Args:
            request: The Flask request object

        Returns:
            User: The User instance or None if not authenticated
        """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        base64_auth = self.extract_base64_authorization_header(auth_header)
        if base64_auth is None:
            return None
        decoded_auth = self.decode_base64_authorization_header(base64_auth)
        if decoded_auth is None:
            return None
        email, password = self.extract_user_credentials(decoded_auth)
        if email is None or password is None:
            return None
        return self.user_object_from_credentials(email, password)
