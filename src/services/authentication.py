"""
The user database is shared between api and web component. Users can only be added through web.

background: http://cryto.net/~joepie91/blog/2016/06/13/stop-using-jwt-for-sessions/
            https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
"""
from functools import wraps

from flask import g, abort, request
from pony.orm import *

from src.start import get_db, get_users_db

udb = get_users_db()


def auth_required(f):
    @db_session
    @wraps(f)
    def wrapper(*args, **kwargs):
        headers = request.headers.get("Authorization").split()  # Basic key-123-abc
        if not headers:
            abort(403)
        api_key = headers[1]
        user = udb.User.get(api_key=api_key)
        if not user:
            abort(403)
        g.user = user
        return f(*args, **kwargs)
    return wrapper
