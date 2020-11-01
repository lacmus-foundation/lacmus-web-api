from pydantic import BaseModel
from enum import auto
from fastapi_utils.enums import StrEnum
from typing import List
from core.processing import Processing



class StatusEnum(StrEnum):
    success = auto()
    failed = auto()

class ProjectCreateResult(BaseModel):
    id: str="" # there is no reason to return id from ftp API added for unification with Identity API
    status: StatusEnum

def createProject(users:List[str],id:str,description:str):
    if len(users)==0:
        return ProjectCreateResult(status=StatusEnum.failed)
    if len(id)==0:
        return ProjectCreateResult(status=StatusEnum.failed)
    try:
        Processing.create_project(users,id,description)
    except:
        return ProjectCreateResult(status=StatusEnum.failed)

    return ProjectCreateResult(status=StatusEnum.success)