from pydantic import BaseModel
from typing import List
from enum import auto

class Object(BaseModel):
    xmin: int
    xmax: int
    ymin: int
    ymax: int
    label: str

class Result(BaseModel):
    objects: List[Object]

