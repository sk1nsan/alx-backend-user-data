#!/usr/bin/env python3
"""Session_authentication module.
"""
from .auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """SessionAuth class.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ create a session for the given user """
        if not user_id:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id
