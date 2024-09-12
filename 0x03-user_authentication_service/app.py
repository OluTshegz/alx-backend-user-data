#!/usr/bin/env python3
"""The Flask app"""

from auth import Auth
from flask import (Flask, jsonify, Response, request,
                   abort, make_response, redirect)


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=['GET'])
def welcome() -> Response:
    """This method contsaisn the GET route for /.
    Returns:
        JSON: the payload."""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'])
def users():
    """Registers a new user"""
    # Get the email and password from form data
    email = request.form.get('email')
    password = request.form.get('password')

    # Check for validity of provided email and password
    if not email or not password:
        abort(400, description="Missing email or password")

    try:
        # Attempt to register the new user
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        # If user exists, return error message
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'])
def login() -> Response:
    """Log into the application!"""

    # Get the email and password from form data
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if email or password are provided
    if not email or not password:
        abort(400, description="Missing email or password")

    # Check validity of login information
    if not AUTH.valid_login(email, password):
        abort(401, description="Unauthorized")
    new_sess = AUTH.create_session(email)

    # create response
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    # Set cookie
    response.set_cookie("session_id", new_sess)
    return response


@app.route("/sessions", methods=["DELETE"])
def logout():
    """
    Log out a user by destroying their session.
    """
    # Get session_id from cookie
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)

    if user:
        # Destroy the session
        AUTH.destroy_session(user.id)
        # Redirect to home page
        return redirect("/")

    # If no user found, return 403 Forbidden status code
    abort(403)


@app.route("/profile", methods=["GET"])
def profile():
    """
    Retrieve the profile of a logged-in user using their session_id.
    """
    # Get session_id from cookie
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)

    if user:
        # Return user's email if found
        return jsonify({"email": user.email}), 200

    # If no user is found, return 403 Forbidden status code
    abort(403)


@app.route("/reset_password", methods=["POST"])
def reset_password():
    """Initiates password reset process for a user."""
    email = request.form.get("email")

    if not email:
        return abort(400, description="Missing email in request")

    try:
        reset_token = AUTH.get_reset_password_token(email)
        # Simulate sending an email with reset token
        # (replace with actual email sending logic)
        # print(f"Reset password token for {email} is: {reset_token}")
        return jsonify({"email": email, "reset_token": reset_token}), 200
        # Send email with reset token (implementation omitted for brevity)
        # return jsonify({"message": "Reset password instructions sent"}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 403


@app.route('/reset_password', methods=['PUT'])
def update_password() -> str:
    """ PUT /reset_password
    Updates password with reset token
    Return:
        - 400 if bad request
        - 403 if not valid reset token
        - 200 and JSON Payload if valid
    """
    try:
        email = request.form['email']
        reset_token = request.form['reset_token']
        new_password = request.form['new_password']
    except KeyError:
        abort(400)

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    msg = {"email": email, "message": "Password updated"}
    return jsonify(msg), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
