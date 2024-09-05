#!/usr/bin/env python3
"""
Route module for the API
"""
# from api.v1.auth.auth import Auth
# from api.v1.auth.basic_auth import BasicAuth
# from api.v1.auth.session_auth import SessionAuth
# from api.v1.auth.session_exp_auth import SessionExpAuth
# from api.v1.auth.session_db_auth import SessionDBAuth
from api.v1.views import app_views
# from models import storage
from flask import Flask, jsonify, abort, request
# from flask import Response
from flask_cors import (CORS, cross_origin)
import os
from os import getenv
# from typing import Literal


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
# Initialize auth to None
auth = None
# Load and assign the correct authentication class
# based on the AUTH_TYPE environment variable
# AUTH_TYPE = os.getenv('AUTH_TYPE', None)
AUTH_TYPE = os.getenv('AUTH_TYPE')

# Instantiate the appropriate authentication
# class based on the environment variable
if AUTH_TYPE == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
elif AUTH_TYPE == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif AUTH_TYPE == 'session_auth':
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()

# List of paths that don't require authentication
EXCLUDED_PATHS = ['/api/v1/status', '/api/v1/unauthorized',
                  '/api/v1/forbidden', '/api/v1/auth_session/login/']
# `/api/v1/auth_session/login/`: this endpoint/route is not defined/created,
# so error output is not "blocked" by an authentication system.
# the value of the error output is 'not found'.

# app.config.from_envvar('AUTH_TYPE', default='auth')
# if app.config['AUTH_TYPE'] == 'auth':
#     auth = Auth()

# Create the auth instance based on the AUTH_TYPE environment variable
# if app.config.get('AUTH_TYPE') == 'auth':
#    auth = Auth()


@app.errorhandler(404)
# def not_found(error) -> tuple[Response, Literal[404]]:
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
# def unauthorized(error) -> tuple[Response, Literal[401]]:
def unauthorized(error) -> str:
    """ Handler for 401 Unauthorized error.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
# def forbidden(error) -> tuple[Response, Literal[403]]:
def forbidden(error) -> str:
    """ Handler for 403 Forbidden error.
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request() -> None:
    """Method to filter requests before
    they reach their destination
    Executed before each request
    """
    if not auth or auth is None:
        return  # or pass, do nothing

    if auth:
        # Check if the request path is excluded
        if not auth.require_auth(request.path, EXCLUDED_PATHS):
            return
        # Check if the request path requires authentication
        if auth.require_auth(request.path, EXCLUDED_PATHS):
            # Check if the Authorization header and
            # the session cookie is present/valid
            if auth.authorization_header(
                    request) is None and auth.session_cookie(request) is None:
                abort(401, description="Unauthorized")
            # Set the current_user in the request
            request.current_user = auth.current_user(request)
            # Check if the current user is authenticated
            if auth.current_user(request) is None:
                abort(403, description="Forbidden")
            if request.current_user is None:
                abort(403, description="Forbidden")


# @app.teardown_appcontext
# def teardown_appcontext(exception):
#     """
#     Called after each request to remove
#     the current SQLAlchemy session.
#     """
#     storage.close()


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = int(getenv("API_PORT", "5000"))
    app.run(host=host, port=port, debug=True)
