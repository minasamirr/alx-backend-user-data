#!/usr/bin/env python3
""" Session authentication module """

import uuid
from flask import Blueprint, request, jsonify, make_response
from api.v1.auth.auth import Auth
from models.user import User
from api.v1.app import auth
import os


session_auth_blueprint = Blueprint('session_auth', __name__, url_prefix='/api/v1/auth_session')


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

    @session_auth_blueprint.route('/login/', methods=['POST'], strict_slashes=False)
    def login():
        """ Login a user based on email and password """
        email = request.form.get('email')
        password = request.form.get('password')

        if not email:
            return jsonify({"error": "email missing"}), 400
        if not password:
            return jsonify({"error": "password missing"}), 400

        user = User.search(email)
        if user is None:
            return jsonify({"error": "no user found for this email"}), 404
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401

        session_id = auth.create_session(user.id)
        response = make_response(user.to_json())
        response.set_cookie(os.getenv('SESSION_NAME'), session_id)
        
        return response
