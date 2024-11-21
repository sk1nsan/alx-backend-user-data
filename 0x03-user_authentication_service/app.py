#!/usr/bin/env python3
""" Flask App
"""

from flask import (
    Flask, Response, jsonify, request, abort, make_response, redirect
)
from auth import Auth
from typing import Tuple


AUTH = Auth()

app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """ route for index page
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> Tuple:
    """ route for registering a user
    """
    email = request.form['email']
    password = request.form['password']
    try:
        new_user = AUTH.register_user(email, password)
        return jsonify({
            "email": f"{new_user.email}", "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> Response:
    """ route for logging in
    """
    email = request.form['email']
    password = request.form['password']
    found_user = AUTH.valid_login(email, password)
    if found_user:
        resp = make_response(jsonify(
            {"email": f"{email}", "message": "logged in"}))
        resp.set_cookie("session_id", AUTH.create_session(email))
        return resp
    abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> Response:
    """ route for logging out
    """
    session_id = request.cookies.get('session_id')
    found_user = AUTH.get_user_from_session_id(session_id)
    if found_user:
        AUTH.destroy_session(found_user.id)
        return redirect("/")
    abort(403)


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> Response:
    """ route for user profile
    """
    session_id = request.cookies.get('session_id')
    found_user = AUTH.get_user_from_session_id(session_id)
    if found_user:
        return jsonify({"email": f"{found_user.email}"})
    abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> Response:
    """ route for resetting password
    """
    email = request.form['email']
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": f"{email}", "reset_token": f"{reset_token}"})
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> Response:
    """ route for updatting password
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
