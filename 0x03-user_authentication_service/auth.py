#!/usr/bin/env python3
"""
Auth module for user authentication.
"""
import bcrypt
from db import DB
from sqlalchemy.exc import IntegrityError
import uuid


def _hash_password(password: str) -> bytes:
    """Hash a password with bcrypt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


class Auth:
    """Auth class to handle user registration and authentication."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user."""
        try:
            self._db.add_user(email, _hash_password(password))
        except IntegrityError:
            raise ValueError(f"User {email} already exists.")
        return self._db.find_user_by(email=email)

    def valid_login(self, email: str, password: str) -> bool:
        """Validate login credentials."""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                password.encode(), user.hashed_password.encode())
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Create a new session for the user."""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            user.session_id = session_id
            self._db._session.commit()
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Find user by session ID."""
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy user session."""
        user = self._db.find_user_by(id=user_id)
        user.session_id = None
        self._db._session.commit()


def _generate_uuid() -> str:
    """Generate a new UUID."""
    return str(uuid.uuid4())
