from typing import final

from pydantic_settings import BaseSettings, SettingsConfigDict


@final
class Settings(BaseSettings):
    """
    Import variables from .env
    """
    API_ID: int
    API_HASH: str
    MINIO_ROOT_USER: str = 'minio_user'
    MINIO_ROOT_PASSWORD: str = 'minio_password'
    MINIO_SERVER_HOST: str = '127.0.0.1'
    MINIO_SERVER_PORT: str = '9000'
    MONGO_USER: str = 'mongo-user'
    MONGO_PASSWORD: str = 'mongo-password'
    MONGO_HOST: str = 'localhost'
    MONGO_PORT: str = '27027'

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
