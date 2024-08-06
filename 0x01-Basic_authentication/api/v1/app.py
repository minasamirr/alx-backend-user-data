#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.auth.auth import Auth


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


# Initialize the auth variable
auth = None

# Load authentication based on AUTH_TYPE
auth_type = os.getenv('AUTH_TYPE')
if auth_type == 'auth':
    auth = Auth()


@app.before_request
def before_request():
    """Check if request is authorized before processing it"""
    if auth is None:
        return
    # List of public endpoints that do not require authentication
    public_endpoints = ['/api/v1/status/',
                        '/api/v1/unauthorized/', '/api/v1/forbidden/']
    if request.path not in public_endpoints and (auth.require_auth(request.path, public_endpoints)):
        if auth.authorization_header(request) is None:
            abort(401)  # Unauthorized
        if auth.current_user(request) is None:
            abort(403)  # Forbidden


@app.route('/api/v1/status/', methods=['GET'])
def status():
    return jsonify({"status": "OK"})


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
