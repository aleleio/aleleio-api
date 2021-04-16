from pathlib import Path

import fastapi

from starlette.staticfiles import StaticFiles

from src.config import Settings
from src.views import games, terms, meta, home

settings = Settings()
api = fastapi.FastAPI()


def configure():
    """Configure the application
    Get settings with os.getenv() and use settings object in the future
    ToDo: https://fastapi.tiangolo.com/advanced/settings/#pydantic-settings
    """
    configure_routing()


def configure_routing():
    """Set all routes
    FastAPI's routers are similar to Flask Blueprints
    """
    project_root = Path(__file__).parent.parent
    static_path = project_root.joinpath('src', 'static')
    api.mount('/static', StaticFiles(directory=static_path), name='static')

    api.include_router(home.router)
    api.include_router(games.router)
    api.include_router(terms.router)
    api.include_router(meta.router)
