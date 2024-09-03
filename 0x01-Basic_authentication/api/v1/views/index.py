#!/usr/bin/env python3
""" Module of Index views
"""
from api.v1.views import app_views
from flask import jsonify, abort
# from flask import Response


@app_views.route('/status', methods=['GET'], strict_slashes=False)
# def status() -> Response:
def status() -> str:
    """ GET /api/v1/status
    Return:
      - the status of the API
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', methods=['GET'], strict_slashes=False)
# def stats() -> Response:
def stats() -> str:
    """ GET /api/v1/stats
    Return:
      - the number of each objects
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def unauthorized() -> str:
    """ GET /api/v1/unauthorized
    Endpoint that raises a 401 Unauthorized error.
    Return:
      - abort with 401 status
    """
    abort(401)


@app_views.route('/forbidden', methods=['GET'], strict_slashes=False)
def forbidden() -> str:
    """ GET /api/v1/forbidden
    Endpoint that raises a 403 Forbidden error.
    Return:
      - abort with 403 status
    """
    abort(403)
