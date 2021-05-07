
from pydantic.class_validators import validator
from pydantic.env_settings import BaseSettings


class Settings(BaseSettings):
    """Parse environment variables into a settings object
    Envars can be provided through a .env file for local development.
    """
    version: str = '0.0.0'
    development: bool = False
    testing: bool = False

    db_host: str = 'localhost'
    db_user: str = ''
    db_password: str = ''
    db_games: str = 'db_games'
    db_users: str = 'db_users'

    def generate_db_dict(cls, v, values):
        """Output a dictionary with the correct settings for development or production database
        db_games and db_users are called via the decorator functions below and receive the validator value as "v".
        """

        if 'development' in values:
            filename = v + '.sqlite'
            return {'provider': 'sqlite', 'filename': filename, 'create_db': True}
        if 'testing' in values:
            return {'provider': 'sqlite', 'filename': ':memory:'}
        else:
            return {
                'provider': 'mysql',
                'host': values.get('db_host'),
                'user': values.get('db_user'),
                'passwd': values.get('db_password'),
                'db': v,
            }

    # Closures/Decorators: func()()
    # This works like a decorator on generate_db_dict()
    # The assignment is used to activate them, will be exectued when e.g. settings.db_games is called in main.py
    _generate_games_dict = validator("db_games", always=True, allow_reuse=True)(generate_db_dict)
    _generate_users_dict = validator("db_users", allow_reuse=True)(generate_db_dict)

