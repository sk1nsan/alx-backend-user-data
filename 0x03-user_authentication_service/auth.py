#!/usr/bin/env python3
""" Auth file
"""
import bcrypt

from db import DB
from user import User
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

    def _generate_uuid(self) -> str:
        return str(uuid.uuid4())


def _hash_password(password: str) -> bytes:
    """ return a salted hash of the input password
    """
    hashed = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
    return hashed
