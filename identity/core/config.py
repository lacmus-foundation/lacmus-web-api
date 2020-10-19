from typing import List
from functools import lru_cache
from pydantic import BaseSettings

# https://github.com/tiangolo/fastapi/issues/508#issuecomment-532360198
class WorkerConfig(BaseSettings):
    project_name: str = "Lacmus ml worker"
    api_prefix: str = "/api/v0"
    version: str = "0.1.0"
    debug: bool = False

    db_user: str = "test"
    db_password: str = "password"
    db_host: str = "postgres"
    db_port: int = 5432
    db_name: str = "example"

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

@lru_cache()
def get_config() -> WorkerConfig:
    return WorkerConfig()