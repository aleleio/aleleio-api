from pathlib import Path

import fastapi

from starlette.staticfiles import StaticFiles
from pony.orm import set_sql_debug

from src.config import Settings
from src.models import db_games, db_users


project_root = Path(__file__).parent.parent
env_path = project_root.joinpath('.env')

settings = Settings(_env_file=env_path)
api = fastapi.FastAPI(
    title='alele.io API',
    description='This is the API documentation for the teambuilding app alele.io',
    version=settings.version,
)


def configure():
    """Configure the application
    Get settings with os.getenv() and use settings object in the future
    ToDo: https://fastapi.tiangolo.com/advanced/settings/#pydantic-settings
    """
    init_database()
    configure_routing()


def init_database():
    """Bind ORM to database
    Settings are prepared in pydantic Settings class (/src/config.py)
    Different database settings, depending on whether envar 'DEVELOPMENT' is set
    """
    db_games.bind(**settings.database_games)
    db_games.generate_mapping(create_tables=True)

    db_users.bind(**settings.database_users)
    db_users.generate_mapping(create_tables=True)

    set_sql_debug(True)


def configure_routing():
    """Set all routes
    FastAPI routers are similar to Flask blueprints
    """
    static_path = project_root.joinpath('src', 'static')
    api.mount('/static', StaticFiles(directory=static_path), name='static')

    from src.views import games, terms, meta, home
    api.include_router(home.router)
    api.include_router(games.router)
    api.include_router(terms.router)
    api.include_router(meta.router)
