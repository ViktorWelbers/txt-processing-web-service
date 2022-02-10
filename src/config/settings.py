from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    upload_folder = "files"


@lru_cache()
def get_settings() -> Settings:
    return Settings()