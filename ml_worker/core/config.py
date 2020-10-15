from typing import List
from functools import lru_cache
from pydantic import BaseSettings
from core.ml.enum import InferTypeEnum

# https://github.com/tiangolo/fastapi/issues/508#issuecomment-532360198
class WorkerConfig(BaseSettings):
    project_name: str = "Lacmus ml worker"
    api_prefix: str = "/api/v0"
    version: str = "0.1.0"
    debug: bool = False

    weights: str = "./snapshotes/lacmus-1-4.h5"
    min_side: int = 800
    max_side: int = 1333
    backbone: str = "resnet50"
    labels: dict = {0: 'Person'}
    infer_type: InferTypeEnum = InferTypeEnum.cpu   

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

@lru_cache()
def get_config() -> WorkerConfig:
    return WorkerConfig()