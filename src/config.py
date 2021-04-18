
from pydantic.class_validators import validator
from pydantic.env_settings import BaseSettings


class Settings(BaseSettings):
    """Parse environment variables into a settings object
    Envars can be provided through a .env file for local development.
    """
    version: str = '0.0.0'
    development: bool = False

    db_host: str = 'localhost'
    db_user: str = ''
    db_password: str = ''
    db_database_games: str = 'db_games'
    db_database_users: str = 'db_users'
    database_games: str = ''
    database_users: str = ''

    def populate_database(cls, v, values):
        """Create a dict with the correct settings for development or production database
        Achived through this reusable validator, which collects the validated values and uses them to complete
        the attributes 'database_games' and 'database_users'.
        """
        if 'database_games' in values:
            current = values.get('db_database_users')
        else:
            current = values.get('db_database_games')

        if 'development' in values:
            filename = current + '.sqlite'
            return {'provider': 'sqlite', 'filename': filename, 'create_db': True}
        else:
            return {
                'provider': 'mysql',
                'host': values.get('db_host'),
                'user': values.get('db_user'),
                'passwd': values.get('db_password'),
                'db': current
            }

    # Closures/Decorators: func()()
    # assignment used to execute classmethod
    _check_games = validator("database_games", always=True, allow_reuse=True)(populate_database)
    _check_users = validator("database_users", allow_reuse=True)(populate_database)

