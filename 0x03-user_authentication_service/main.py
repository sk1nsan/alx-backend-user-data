#!/usr/bin/env python3
"""
Main file
"""

import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """ test for registering a new user
    """
    payload = {'email': email, 'password': password}
    r = requests.post('http://localhost:5000/users', data=payload)
    assert (r.json() == {"email": email, "message": "user created"})


def log_in_wrong_password(email: str, password: str) -> None:
    """ test for logging in with wrong password
    """
    payload = {'email': email, 'password': password}
    r = requests.post('http://localhost:5000/sessions', data=payload)
    assert (r.status_code == 401)


def log_in(email: str, password: str) -> str:
    """ test for logging with correct password
    """
    payload = {'email': email, 'password': password}
    r = requests.post('http://localhost:5000/sessions', data=payload)
    session_id = r.cookies.get('session_id')
    assert (r.json() == {"email": email, "message": "logged in"})
    return session_id


def profile_unlogged() -> None:
    """ test for viewing profile with no active session
    """
    r = requests.get('http://localhost:5000/profile')
    assert (r.status_code == 403)


def profile_logged(session_id: str) -> None:
    """ test for viewing profile with active session
    """
    cookies = {'session_id': session_id}
    r = requests.get('http://localhost:5000/profile', cookies=cookies)
    assert (r.json() == {"email": EMAIL})


def log_out(session_id: str) -> None:
    """ test for logging out
    """
    cookies = {'session_id': session_id}
    r = requests.delete('http://localhost:5000/sessions', cookies=cookies)
    assert (r.json() == {"message": "Bienvenue"})


def reset_password_token(email: str) -> str:
    """ test for getting reset_token
    """
    payload = {'email': email}
    r = requests.post('http://localhost:5000/reset_password', data=payload)
    assert (r.status_code == 200)
    reset_token = r.json().get('reset_token')
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ test for updatting password
    """
    payload = {'email': email, 'reset_token': reset_token,
               'new_password': new_password}
    r = requests.put('http://localhost:5000/reset_password', data=payload)
    assert (r.json() == {"email": email, "message": "Password updated"})


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
