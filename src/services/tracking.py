from datetime import datetime

from flask import g
from pony.orm import desc

from src.start import get_db

db = get_db()
udb = get_db(users_db=True)


def get_session(request):
    """Track user session, renew by activity within 5min window
    Requests to the API may come in from web interface, mobile apps or direct api calls and are identified by api-key.
    Apps will send api-keys of logged-in users, otherwise use their own.
    """
    user = udb.User[g.uid]
    session_params = dict(user_id=g.uid)

    if user.login in ["web", "android", "ios"]:  # pragma: no cover
        session_params.update(
            origin=user.login,
            remote_addr=request.headers.get("X-Remote-Addr"),
            user_agent=request.headers.get("X-User-Agent"),
        )
        session = anon_session(session_params)
    else:
        session_params.update(
            origin=request.headers.get("X-Origin", "api"),
            remote_addr=request.remote_addr,
            user_agent=request.headers.get("User-Agent"),
        )
        session = logged_in_session(session_params)

    return session


def anon_session(session_params):  # pragma: no cover
    user_sessions = db.Session.select(lambda s: s.remote_addr == session_params["remote_addr"])
    return get_active_session(user_sessions, session_params)


def logged_in_session(session_params):
    user_sessions = db.Session.select(lambda s: s.user_id == session_params["user_id"])
    return get_active_session(user_sessions, session_params)


def get_active_session(user_sessions, session_params):
    if user_sessions:
        last_session = user_sessions.sort_by(desc(db.Session.starttime))[:1][0]
        timedelta = datetime.utcnow() - last_session.endtime
        if timedelta.seconds < 300:
            last_session.endtime = datetime.utcnow()
            return last_session
    return db.Session(**session_params)


def add_request(session, request, response):
    r_object = db.Request(
        session=session,
        path=request.path,
        method=request.method
    )

    add_request_is_query(r_object, request, response)
    add_request_is_names(request, response)
    add_request_is_single_game(r_object, request)


def add_request_is_query(r_object, request, response):
    query = request.values
    if query:
        r_object.query_type = "group_needs" if "main" in query.keys() else "basic"
        add_request_query_params(r_object, query)

    if type(response.json) is list:
        r_object.result_length = len(response.json)


def add_request_query_params(r_object, query):
    for param, value in query.items():
        if param == "limit":
            r_object.result_limit = value
        else:
            r_object.query_params.add(db.QueryParam.get(slug=value))


def add_request_is_names(request, response):
    if request.path == "/names":
        for item in response.json:
            game_stat = db.GameStatistic.get(game_id=item["game_id"])
            game_stat.search_impressions += 1


def add_request_is_single_game(r_object, request):
    if request.path[:7] == "/games/":
        game_id = int(request.path[7:])
        r_object.game_id = game_id
        if request.method == "GET":
            game_stat = db.GameStatistic.get(game_id=game_id)
            game_stat.detail_impressions += 1
            game_stat.last_impression = datetime.utcnow()
