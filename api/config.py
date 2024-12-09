import os
import pathlib
from functools import lru_cache

from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings
                 ):
    BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent

    DATABASE_URL: str = os.environ.get("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@db:5432/legendary-octo-guide")
    SYNC_DATABASE_URL: str = os.environ.get("SYNC_DATABASE_URL", "postgresql://postgres:postgres@db:5432/legendary-octo-guide")
    DATABASE_CONNECT_DICT: dict = {}
    ENV: str = "development"


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass


class Settings(BaseSettings):
    FASTAPI_CONFIG: str = "development"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    settings = Settings()
    config_cls_dict = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig
    }

    config_name = settings.FASTAPI_CONFIG
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()