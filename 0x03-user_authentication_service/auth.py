#!/usr/bin/env python3
"""
Authentication module for handling user registration and login.
"""

import bcrypt
import uuid
from sqlalchemy.exc import NoResultFound
from db import DB
from user import User


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        """Initialize the Auth instance."""
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """
        Hash a password with bcrypt.

        Parameters:
        - password (str): The password to hash.

        Returns:
        - bytes: The hashed password.
        """
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user.

        Parameters:
        - email (str): The user's email.
        - password (str): The user's password.

        Returns:
        - User: The registered User object.

        Raises:
        - ValueError: If the user already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = self._hash_password(password)
            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate login credentials.

        Parameters:
        - email (str): The user's email.
        - password (str): The user's password.

        Returns:
        - bool: True if credentials are valid, otherwise False.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                password.encode('utf-8'), user.hashed_password)
        except NoResultFound:
            return False

    def _generate_uuid(self) -> str:
        """
        Generate a new UUID.

        Returns:
        - str: The new UUID.
        """
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """
        Create a session for the user.

        Parameters:
        - email (str): The user's email.

        Returns:
        - str: The session ID.
        """
        user = self._db.find_user_by(email=email)
        session_id = self._generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Get a user by session ID.

        Parameters:
        - session_id (str): The session ID.

        Returns:
        - User: The corresponding User object, or None if not found.
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy a user's session.

        Parameters:
        - user_id (int): The ID of the user whose session will be destroyed.
        """
        self._db.update_user(user_id, session_id=None)
