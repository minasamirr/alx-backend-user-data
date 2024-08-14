#!/usr/bin/env python3
"""
Basic Flask app for user authentication.
"""

from flask import Flask, jsonify, request, abort
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def index():
    """Return a welcome message."""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register_user():
    """Register a new user."""
    email = request.form.get("email")
    password = request.form.get("password")
    if not email or not password:
        abort(400, description="Email and password are required")
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """Log in a user and create a session."""
    email = request.form.get("email")
    password = request.form.get("password")
    if not email or not password:
        abort(400, description="Email and password are required")
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    else:
        abort(401)


@app.route("/sessions", methods=["DELETE"])
def logout():
    """Log out a user and destroy the session."""
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(401)
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return jsonify({"message": "logged out"})
    else:
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
