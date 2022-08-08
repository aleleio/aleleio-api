import os
from functools import lru_cache
from pathlib import Path

import yaml
from connexion import FlaskApp
from connexion.resolver import RelativeResolver
from dotenv import load_dotenv


@lru_cache()
def get_project_root():
    return Path(__file__).parent.parent


@lru_cache()
def get_project_version():
    """Get the current version from openapi.yml config file.
    """
    yml_path = Path(get_project_root(), 'openapi.yml')
    with open(yml_path, 'r') as fin:
        yml = yaml.safe_load(fin)

    return yml['info']['version']


def get_app():
    """Connexion Wrapper App
    Connexion creates a wrapper around a Flask app, through which all requests are passed.
    The Connexion wrapper app is called by wsgi.py and pytest.
    You can access the Flask app with `app.app.properties`.
    """

    # Load Environment Variables from dotenv file
    dotenv_path = Path(get_project_root(), '.env')
    load_dotenv(dotenv_path)

    # Todo: Sentry integration
    # sentry_sdk.init(
    #     dsn=os.environ('SENTRY_DSN'),
    #     integrations=[FlaskIntegration()],
    #     # Reduce this for production, maybe 0.25
    #     traces_sample_rate=0.25,
    #     release=get_project_version(),
    #     environment=Config().SENTRY
    # )

    swagger_options = {
        'swagger_url': '/',
        'swagger_ui_config': {
            'operationsSorter': 'method',
            'tagsSorter': 'alpha',
        }
    }
    connexion_app = FlaskApp(__name__, specification_dir=get_project_root(), options=swagger_options)
    connexion_app.add_api('openapi.yml', resolver=RelativeResolver('src.views'), validate_responses=True)
    connexion_app.app.config.from_prefixed_env(prefix='API')
    return connexion_app
