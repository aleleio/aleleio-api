from pydantic.env_settings import BaseSettings
from pydantic.networks import RedisDsn, PostgresDsn


class Settings(BaseSettings):
    """Parse environment variables into a settings object
    Envars can be provided through a .env file for local development.
    """
    version: str = '0.0.0'
    secret_key: str = 'set-a-secret-key!'

