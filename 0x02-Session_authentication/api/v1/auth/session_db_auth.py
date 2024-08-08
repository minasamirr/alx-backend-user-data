#!/usr/bin/env python3
""" session_db_auth module
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    def create_session(self, user_id=None):
        """ Create a session and store it in the database """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Return the user_id for a session_id from the database """
        if session_id is None:
            return None

        try:
            user_session = UserSession.find_by(session_id=session_id)
            if user_session is None:
                return None

            if self.session_duration > 0:
                created_at = user_session.created_at
                addTime = created_at + timedelta(
                    seconds=self.session_duration)
                if created_at is None or datetime.now() > addTime:
                    return None

            return user_session.user_id
        except Exception:
            return None

    def destroy_session(self, request=None):
        """ Delete a session from the database """
        if not super().destroy_session(request):
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        try:
            user_session = UserSession.find_by(session_id=session_id)
            if user_session is None:
                return False

            user_session.delete()
            return True
        except Exception:
            return False
