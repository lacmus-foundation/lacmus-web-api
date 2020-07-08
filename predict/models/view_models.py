from pydantic import BaseModel, Field
from pydantic.types import List

class Files(BaseModel):
    files: List[str]

class Tasks(BaseModel):
    tasks: List[str]

class TaskResult(BaseModel):
    success: bool = True
    status: str = 'done'
    annotation_id: int = 0

class Error(BaseModel):
    detail: str = 'error description'