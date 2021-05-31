from pathlib import Path
from typing import Optional

from pydantic.class_validators import validator
from pydantic.env_settings import BaseSettings


class Settings(BaseSettings):
    """Parse environment variables into a settings object
    Envars can be provided through a .env file for local development.
    Do not give bools a default value, they should only be checked for presence.
    """
    version: str = '0.0.0'
    production: Optional[bool]
    testing: Optional[bool]

    db_host: str = 'localhost'
    db_user: str = ''
    db_password: str = ''
    db_games: str = 'db_games'
    db_users: str = 'db_users'
    get_db_connection: dict = None

    class Config:
        env_file = '.env'
        print('pydantic config: ', Path('.env').resolve())

    @validator('get_db_connection')
    def generate_db_dict(cls, validator_value, values):
        """Output a dictionary with the correct settings for development or production database
        """
        if values.get('production') is not None:
            return {
                'provider': 'mysql',
                'host': values.get('db_host'),
                'user': values.get('db_user'),
                'passwd': values.get('db_password'),
                'db': 'db_aleleio',
            }
        elif values.get('testing') is not None:
            return {'provider': 'sqlite', 'filename': ':memory:'}
        else:
            filename = 'db_aleleio.sqlite'
            return {'provider': 'sqlite', 'filename': filename, 'create_db': True}
