from typing import List
from functools import lru_cache
from pydantic import BaseSettings


# https://github.com/tiangolo/fastapi/issues/508#issuecomment-532360198
class WorkerConfig(BaseSettings):
    project_name: str = "Lacmus ml worker with Yolo v5 model"
    api_prefix: str = "/api/v0"
    version: str = "0.1.0"
    debug: bool = False

    weights: str = "./model/snapshotes/yolo5_fullDS_native.pt"
    iou = 0.20
    conf = 0.05
    image_size = 1984
    labels: dict = {0: 'Person'}

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

@lru_cache()
def get_config() -> WorkerConfig:
    return WorkerConfig()