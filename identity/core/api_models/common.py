from pydantic import BaseModel
from fastapi_utils.enums import StrEnum
from enum import auto

class Pong(BaseModel):
    pong: str = "Lacmus web API, version X.Y.Z"

class RoleEnum(StrEnum):
    root = 0
    admin = 1
    user = 2

class TaskStatusEnum(StrEnum):
    active = 0
    finished = 1
    failed = 2