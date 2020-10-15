from pydantic import BaseModel
from typing import List
from enum import auto
from fastapi_utils.enums import StrEnum

class StatusEnum(StrEnum):
    in_progress = auto()
    finished = auto()
    failed = auto()

class Object(BaseModel):
    xmin: int
    xmax: int
    ymin: int
    ymax: int
    label: str

class Result(BaseModel):
    status: StatusEnum
    objects: List[Object]

