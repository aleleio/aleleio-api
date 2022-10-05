from datetime import datetime

from flask import g
from pony.orm import db_session, desc

from src.start import get_db

db = get_db()
udb = get_db(users_db=True)


def get_session(request):
    """Track user session for 5 minutes
    Requests to the API may come in from web interface, mobile apps or direct api calls and are identified by api-key.
    Apps will send api-keys of logged-in users, otherwise use their own.
    """
    user = udb.User[g.uid]
    session_params = dict(user_id=g.uid)

    if user.login in ["web", "android", "ios"]:
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


def anon_session(session_params):
    user_sessions = db.Session.select(lambda s: s.remote_addr == session_params["remote_addr"])
    return get_active_session(user_sessions, session_params)


def logged_in_session(session_params):
    user_sessions = db.Session.select(lambda s: s.user_id == session_params["user_id"])
    return get_active_session(user_sessions, session_params)


def get_active_session(user_sessions, session_params):
    if user_sessions:
        last_session = user_sessions.sort_by(desc(db.Session.starttime))[:1][0]
        timedelta = datetime.utcnow() - last_session.starttime
        if timedelta.seconds < 300:
            last_session.endtime = datetime.utcnow()
            return last_session
    return db.Session(**session_params)


def add_request(session, request):
    # query_params Set(QueryParam)
    # query_type Optional(str)
    # game_id Optional(int)
    # result_length Optional(int)
    this = db.Request(
        session=session,
        path=request.path,
        method=request.method
    )



@db_session
def get_all_names(user, filters, result):
    """
    Save entry to API Statistics and create/update entry in Game Statistics.
    get_all_names is relevant because it is used for list-view in web component.
    Todo: add group_needs filter
    :param user:
    :param filters:
    :param result:
    :return:
    """

    # Names need to be reduced to unique games
    games_result = set()

    for name in result:
        game_id = name.get('game', '')
        games_result.add(game_id)

    # API Statistics
    api_stat_object = db.QueryStatistic(
        user_id=user.id,
        request_origin=user.request_origin,
        request_uri="names",
        request_type="GET",
        request_result=len(games_result)
    )

    params_object = db.QueryStatisticParam(stat_entry=api_stat_object)
    if 'game_type' in filters:
        params_object.game_type = filters['game_type']
    if 'game_length' in filters:
        params_object.game_length = filters['game_length']
    if 'group_size' in filters:
        params_object.group_size = filters['group_size']
    if 'limit' in filters:
        params_object.limit = filters['limit']

    # Game Statistics
    for game_id in games_result:
        game_stat_object = db.GameStatistic.select(lambda s: s.game.id == game_id).get()
        if not game_stat_object:
            game_stat_object = db.GameStatistic(game=db.Game[game_id])
            game_stat_object.search_impressions = 1
        elif not game_stat_object.search_impressions:
            game_stat_object.search_impressions = 1
        else:
            game_stat_object.search_impressions += 1


@db_session
def get_all_games(user, filters, result):
    """
    Save entry to API Statistics only.
    get_all_games is not used to display games in web component, therefore not relevant for impressions.
    Todo: add group_needs filter
    :param user:
    :param filters:
    :param result:
    :return:
    """

    # API Statistics
    api_stat_object = db.QueryStatistic(
        user_id=user.id,
        request_origin=user.request_origin,
        request_uri="games",
        request_type="GET",
        request_result=len(result)
    )

    params_object = db.QueryStatisticParam(stat_entry=api_stat_object)
    if 'game_type' in filters:
        params_object.game_type = filters['game_type']
    if 'game_length' in filters:
        params_object.game_length = filters['game_length']
    if 'group_size' in filters:
        params_object.group_size = filters['group_size']
    if 'limit' in filters:
        params_object.limit = filters['limit']


@db_session
def get_single_game(user, game_id):
    """
    Save entry to API Statistics and create/update entry in Game Statistics when a single game is requested.
    :param user_id:
    :param game_id:
    :return:
    """

    # API Statistics
    db.AAPIPIStatistics(
        user_id=user.id,
        request_origin=user.request_origin,
        request_uri="games/id",
        request_type="GET",
        request_game_id=game_id
    )

    # Game Statistics
    game_stat_object = db.GameStatistic.select(lambda s: s.game.id == game_id).get()

    if not game_stat_object:
        game_stat_object = db.GameStatistic(game=db.Game[game_id])
        game_stat_object.detail_impressions = 1
    elif not game_stat_object.detail_impressions:
        game_stat_object.detail_impressions = 1
    else:
        game_stat_object.detail_impressions += 1

    game_stat_object.last_impression = datetime.datetime.utcnow()


@db_session
def post_games(user, result):
    """
    Save entries to API Statistics when new games are created.
    :param user:
    :param result:
    :return:
    """

    db.QueryStatistic(
        user_id=user.id,
        request_origin=user.request_origin,
        request_uri="games",
        request_type="POST",
        request_result=len(result)
    )


@db_session
def patch_game(user, game_id):
    """
    Save entry to API Statistics when a game is changed.
    :param user:
    :param game_id:
    :return:
    """

    db.QueryStatistic(
        user_id=user.id,
        request_origin=user.request_origin,
        request_uri="games/id",
        request_type="PATCH",
        request_game_id=game_id
    )


@db_session
def delete_game(user, game_id):
    """
    Save entry to API Statistics when a game is deleted.
    :param user:
    :param game_id:
    :return:
    """

    db.QueryStatistic(
        user_id=user.id,
        request_origin=user.request_origin,
        request_uri="games/id",
        request_type="DELETE",
        request_game_id=game_id
    )


@db_session
def get_all_enums(user, result):
    """
    Save entry to API Statistics when enums are requested.
    :param user_id:
    :param result:
    :return:
    """

    db.QueryStatistic(
        user_id=user.id,
        request_origin=user.request_origin,
        request_uri="enums",
        request_type="GET",
        request_result=len(result)
    )


@db_session
def get_all_game_types(user, result):
    """
    Save entry to API Statistics when game_types are requested.
    :param user:
    :param result:
    :return:
    """

    db.QueryStatistic(
        user_id=user.id,
        request_origin=user.request_origin,
        request_uri="game_types",
        request_type="GET",
        request_result=len(result)
    )


@db_session
def get_all_game_lengths(user, result):
    """
    Save entry to API Statistics when game_lengths are requested.
    :param user:
    :param result:
    :return:
    """

    db.QueryStatistic(
        user_id=user.id,
        request_origin=user.request_origin,
        request_uri="game_lengths",
        request_type="GET",
        request_result=len(result)
    )


@db_session
def get_all_group_sizes(user, result):
    """
    Save entry to API Statistics when group_sizes are requested.
    :param user:
    :param result:
    :return:
    """

    db.QueryStatistic(
        user_id=user.id,
        request_origin=user.request_origin,
        request_uri="group_sizes",
        request_type="GET",
        request_result=len(result)
    )


@db_session
def get_all_group_needs(user, result):
    """
    Save entry to API Statistics when group_needs are requested.
    :param user:
    :param result:
    :return:
    """

    db.QueryStatistic(
        user_id=user.id,
        request_origin=user.request_origin,
        request_uri="group_needs",
        request_type="GET",
        request_result=len(result)
    )
