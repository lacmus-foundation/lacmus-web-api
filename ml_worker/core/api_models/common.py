from pydantic import BaseModel
from fastapi_utils.enums import StrEnum
from typing import List
from enum import auto

class Pong(BaseModel):
    pong: str = "Lacmus web API, version X.Y.Z"

class Prediction(BaseModel):
    xmin: int
    ymin: int
    xmax: int
    ymax: int
    score: float
    label: str = 'Pedestrian'

class Result(BaseModel):
    objects: List[Prediction] = None