from pydantic.env_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str = 'set-a-secret-key!'
