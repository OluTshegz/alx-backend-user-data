#!/usr/bin/env python3
"""
Flask view for Session Authentication
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User
from os import getenv


# POST /auth_session/login route definition
@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    Handles the creation of a new session (login) for a user.
    """
    # Retrieve the email from the form data in the POST request
    email = request.form.get('email')
    # If email is missing or empty, return an error response
    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400

    # Retrieve the password from the form data in the POST request
    password = request.form.get('password')
    # If password is missing or empty, return an error response
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400

    # Search for a user in the database with the provided email
    try:
        users = User.search({"email": email})
    except Exception:
        # If there is an error in searching the user, return an error response
        return jsonify({"error": "no user found for this email"}), 404

    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    # If no user was found, return an error response
    if len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]  # Assume the first user is the one we're looking for

    # Check if the provided password is correct
    if not user.is_valid_password(password):
        # If the password is incorrect, return an error response
        return jsonify({"error": "wrong password"}), 401

    # Import auth to create a session ID (avoiding circular import issues)
    from api.v1.app import auth
    # Create a session ID for the user
    session_id = auth.create_session(user.id)

    # Prepare the user's JSON representation to return in the response
    user_json = user.to_json()

    # Get the session name from the environment variables
    session_name = getenv("SESSION_NAME")

    # Create a response with the user JSON and set the session ID as a cookie
    response = jsonify(user_json)
    response.set_cookie(session_name, session_id)

    return response


# DELETE /auth_session/logout route definition
@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """
    Handles the deletion of a user session (logout).
    """
    # Import auth to use the destroy_session
    # method (avoiding circular import issues)
    from api.v1.app import auth

    # Call the destroy_session method to delete the session
    if not auth.destroy_session(request):
        # If destroy_session returns False, abort with a 404 error
        abort(404)

    # Return an empty JSON dictionary with a
    # status code of 200 if logout is successful
    return jsonify({}), 200
