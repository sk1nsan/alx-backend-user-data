#!/usr/bin/env python3
""" Module of session views
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.user import User
import os


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
        out.set_cookie(os.environ.get('SESSION_NAME'), session_id)
        return out


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def session_logout() -> str:
    """ routes for Session deletion / logout """
    from api.v1.app import auth
    is_destoryed = auth.destroy_session(request)
    if is_destoryed:
        return jsonify({}), 200
    abort(404)
