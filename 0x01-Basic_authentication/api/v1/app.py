#!/usr/bin/env python3
"""
Route module for the API
"""
# from api.v1.auth.auth import Auth
# from api.v1.auth.basic_auth import BasicAuth
from api.v1.views import app_views
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
AUTH_TYPE = os.getenv('AUTH_TYPE', None)
if AUTH_TYPE == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
elif AUTH_TYPE == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()

# List of paths that don't require authentication
EXCLUDED_PATHS = ['/api/v1/status',
                  '/api/v1/unauthorized', '/api/v1/forbidden']

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
# def not_forbidden(error) -> tuple[Response, Literal[403]]:
def forbidden(error) -> str:
    """ Handler for 403 Forbidden error.
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request():
    """Method to filter requests before
    they reach their destination"""
    if auth is None:
        return  # or pass, do nothing

    # Check if the request path requires authentication
    if auth.require_auth(request.path, EXCLUDED_PATHS):
        # Check if the Authorization header is present
        if auth.authorization_header(request) is None:
            abort(401, description="Unauthorized")
        # Check if the current user is authenticated
        if auth.current_user(request) is None:
            abort(403, description="Forbidden")


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = int(getenv("API_PORT", "5000"))
    app.run(host=host, port=port)
