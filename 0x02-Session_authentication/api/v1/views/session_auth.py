#!/usr/bin/env python3
""" Module of session views
"""
from api.v1.views import app_views
from flask import jsonify, request
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login() -> str:
    """ routes for Session authentication """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    user = User.search({'email': email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    user = user[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    else:
        from api.v1.app import auth
        session_id = auth.create_session(user.id)
        out = jsonify(user.to_json())
        out.set_cookie('SESSION_NAME', session_id)
        return out
