from functools import lru_cache

from pydantic import BaseSettings

class Configuration(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    SERVER_HOST: str
    SERVER_PORT: int
    LOG_FILE: str
    MYSQL_HOSTNAME: str
    MYSQL_USERNAME: str
    MYSQL_PASSWORD: str
    MYSQL_DBNAME: str

    class Config:
        env_file = ".env"


config = Configuration()

@lru_cache()
def get_settings():
    return Configuration()
