#!/usr/bin/env python3
"""
Flask app with user registration
"""
from flask import Flask, jsonify, redirect, request, abort, make_response
from auth import Auth

app = Flask(__name__)
# Instantiate Auth for user management
AUTH = Auth()


@app.route("/", methods=["GET"])
def index():
    """Basic route returning a welcome message"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register_user():
    """Register a new user via POST request."""
    # Get the email and the password from the form data
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        # Try registering the user
        if email is not None:
            if password is not None:
                user = AUTH.register_user(email, password)
            else:
                return jsonify({"message": "password is required"}), 400
        else:
            return jsonify({"message": "email is required"}), 400
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        # If the user already exists
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """
    Login a user by validating their email and password.
    If valid, creates a session and stores the session ID as a cookie.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    # If login credentials are invalid or missing
    if not AUTH.valid_login(email, password):
        # return 401 Unauthorized status code
        abort(401)

    # Create a session for the user
    session_id = AUTH.create_session(email)
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    # Store session_id in a cookie
    response.set_cookie("session_id", session_id)

    # Return the response with session_id set in the cookie
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
