#!/usr/bin/env python3
""" Session authentication module """

import uuid
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """ SessionAuth class """

    def __init__(self):
        """ Initialize SessionAuth """
        super().__init__()
        self.user_id_by_session_id = {}

    def create_session(self, user_id=None):
        """ Create a new session """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Get user ID from session ID """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> User:
        """ Return a User instance based on a session cookie """
        if request is None:
            return None
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id) if user_id else None
