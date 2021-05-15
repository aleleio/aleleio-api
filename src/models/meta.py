from datetime import datetime

from pony.orm import *

from src.models import db_games


class GameMeta(db_games.Entity):
    game = Required(lambda: db_games.Game)

    timestamp = Required(datetime, default=datetime.utcnow)
    author_id = Required(int)
    license = Optional(str)
    license_url = Optional(str)
    license_owner = Optional(str)
    license_owner_url = Optional(str)


class Reference(db_games.Entity):
    games = Set(lambda: db_games.Game)

    slug = Required(str)
    full = Required(str)
    url = Optional(str)


class Collection(db_games.Entity):
    """Todo: Implement, connect to user (id), add more details
    """
    games = Set(lambda: db_games.Game)

    slug = Required(str)
    full = Required(str)


class Version(db_games.Entity):
    game = Required(lambda: db_games.Game)
    changesets = Set(lambda: VersionChangeset)

    author_id = Required(int)
    timestamp = Required(datetime, default=datetime.utcnow)


class VersionChangeset(db_games.Entity):
    """For each changed entity in a new version of a game,
    track the detailed changes and store them in a VersionChangeset
    (e.g. one changeset for key="name"; an additional name)
    """
    version = Required(Version)

    key = Required(str)
    value = Required(LongStr)
    key_id = Optional(int)
    score = Optional(int)
    url = Optional(str)
    action = Required(str)


class GameStatistic(db_games.Entity):
    """Search statistics for each individual game.
    New in 0.6: Directly link the queries in which a game appeared
    """
    game = Required(lambda: db_games.Game)
    queries = Set(lambda: QueryStatistic)

    search_impressions = Optional(int)
    detail_impressions = Optional(int)
    last_impression = Optional(datetime)


class QueryStatistic(db_games.Entity):
    """API query statistics
    """
    game_statistics = Set(GameStatistic)

    timestamp = Required(datetime, default=datetime.utcnow)
    user_id = Required(int)
    request_origin = Required(str)
    request_uri = Required(str)
    request_type = Required(str)
    request_game_id = Optional(int)
    request_param = Optional(lambda: QueryStatisticParam)
    request_result = Optional(int)


class QueryStatisticParam(db_games.Entity):
    """API query parameters
    New in 0.6: Add group_needs tracking
    """
    query = Required(QueryStatistic)

    query_type = Optional(str)  # basic / group_needs
    game_type = Optional(str)
    game_length = Optional(str)
    group_size = Optional(str)
    main = Optional(str)
    aux1 = Optional(str)
    aux2 = Optional(str)
    limit = Optional(int)
