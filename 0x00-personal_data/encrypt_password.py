#!/usr/bin/env python3
"""
Module for password encryption and validation.
"""

import bcrypt
from typing import Union


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.

    Args:
        password: The password to hash.

    Returns:
        The hashed password as a byte string.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates that the provided password matches the hashed password.

    Args:
        hashed_password: The hashed password.
        password: The password to validate.

    Returns:
        True if the password is valid, False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
