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
