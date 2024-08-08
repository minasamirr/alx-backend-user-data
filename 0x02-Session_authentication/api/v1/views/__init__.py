#!/usr/bin/env python3
""" Initialize all routes for the API
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views.users import *

User.load_from_file()

from .session_auth import session_auth_blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

app_views.register_blueprint(session_auth_blueprint)
