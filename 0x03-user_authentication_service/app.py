#!/usr/bin/env python3
""" Flask App
"""

from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
