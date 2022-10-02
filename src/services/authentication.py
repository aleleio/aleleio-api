"""
The user database is shared between api and web component. Users can only be added through web.

background: http://cryto.net/~joepie91/blog/2016/06/13/stop-using-jwt-for-sessions/
            https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
"""

from flask import abort, g
from pony.orm import *

from src.start import get_db

udb = get_db(users_db=True)


@db_session
def api_key_auth(token, required_scopes):
    user = udb.User.get(api_key=token)
    if not user:
        abort(403)
    g.uid = user.id
    return {"uid": user.id}