from datetime import datetime

from pony.orm import *


def define_entities_api(db):

    class GameStatistic(db.Entity):
        """Search statistics for each individual game.
        New in 0.6: Directly link the queries in which a game appeared
        """
        game = Required(lambda: db.Game)
        queries = Set(lambda: QueryStatistic)

        search_impressions = Optional(int)
        detail_impressions = Optional(int)
        last_impression = Optional(datetime)

    class QueryStatistic(db.Entity):
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

    class QueryStatisticParam(db.Entity):
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
