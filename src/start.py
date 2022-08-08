from functools import lru_cache
from pathlib import Path

from connexion import FlaskApp
from connexion.resolver import RelativeResolver


@lru_cache()
def get_project_root():
    return Path(__file__).parent.parent


def get_app():
    options = {
        'swagger_url': '/',
        'swagger_ui_config': {
            'operationsSorter': 'method',
            'tagsSorter': 'alpha',
        }
    }
    app = FlaskApp(__name__, specification_dir=get_project_root(), options=options)
    app.add_api('openapi.yml', resolver=RelativeResolver('src.views'), validate_responses=True)
    return app
