#!/usr/bin/env python3
""" Auth file
"""
import bcrypt

from db import DB
from user import User
from typing import Union
from sqlalchemy.orm.exc import NoResultFound
import uuid


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ handle basic data validation and hashing
        """
        my_db = self._db
        try:
            found_user = my_db.find_user_by(email=email)
            raise ValueError(f"User {found_user.email} already exists")
        except NoResultFound:
            password = _hash_password(password)
            new_user = my_db.add_user(email=email, hashed_password=password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """ Credentials validation
        """
        my_db = self._db
        try:
            found_user = my_db.find_user_by(email=email)
            return bcrypt.checkpw(str.encode(password),
                                  found_user.hashed_password)

        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """ create a new session
        """
        my_db = self._db
        session_id = _generate_uuid()
        try:
            found_user = my_db.find_user_by(email=email)
            found_user.session_id = session_id
            return session_id
        except NoResultFound:
            return

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """ returns the used corresponding to `session_id` or None if not found
        """
        my_db = self._db
        if not session_id:
            return None
        try:
            found_user = my_db.find_user_by(session_id=session_id)
            return found_user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ destroy session corresponding to `user_id`
        """
        my_db = self._db
        try:
            found_user = my_db.find_user_by(id=user_id)
            found_user.session_id = None
            return None
        except NoResultFound:
            return None


def _hash_password(password: str) -> bytes:
    """ return a salted hash of the input password
    """
    hashed = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
    return hashed


def _generate_uuid() -> str:
    """ return a string representation of a new UUID
    """
    return str(uuid.uuid4())
