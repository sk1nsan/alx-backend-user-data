#!/usr/bin/env python3
""" Auth file
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """ return a salted hash of the input password
    """
    hashed = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
    return hashed
