from pathlib import Path

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from pony.orm import Database, set_sql_debug, db_session

from src.config import Settings
from src.models import GameTypeEnum, GameLengthEnum, GroupSizeEnum, GroupNeedEnum, \
    define_entities_game, define_entities_meta, define_entities_user

###################
# Project Constants

project_root = Path(__file__).parent.parent

settings = Settings()

application = FastAPI(
    title='alele.io API',
    description='This is the API documentation for the teambuilding app alele.io',
    version=settings.version,
)

# Bind ORM to database
database = Database(**settings.get_db_connection)
define_entities_game(database)
define_entities_meta(database)
define_entities_user(database)
database.generate_mapping(create_tables=True)
set_sql_debug(False)

# /Project Constants
####################


def configure(app, db):
    """Configure the application
    """
    seed_database(db)
    configure_routing(app)


@db_session
def seed_database(db):
    if not db.GameType.get(slug="ice"):
        for item in GameTypeEnum:
            db.GameType(slug=item.value, full=item.full)
        for item in GameLengthEnum:
            db.GameLength(slug=item.value, full=item.full)
        for item in GroupSizeEnum:
            db.GroupSize(slug=item.value, full=item.full)
        for item in GroupNeedEnum:
            db.GroupNeed(slug=item.value, full=item.full)


def configure_routing(app):
    """Set all routes
    FastAPI routers are similar to Flask blueprints
    """
    static_path = project_root.joinpath('src', 'static')
    app.mount('/static', StaticFiles(directory=static_path), name='static')

    from src.views import games, terms, meta, home
    app.include_router(home.router)
    app.include_router(games.router)
    app.include_router(terms.router)
    app.include_router(meta.router)
