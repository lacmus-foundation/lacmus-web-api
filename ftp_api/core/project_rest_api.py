from pydantic import BaseModel
from enum import auto
from fastapi_utils.enums import StrEnum
from typing import List
from core.processing import Processing
import logging


class StatusEnum(StrEnum):
    success = auto()
    failed = auto()


class ProjectCreateResult(BaseModel):
    id: str = ""  # there is no reason to return id from ftp API added for unification with Identity API
    status: StatusEnum
    message = ""


def createProject(users: List[str], id: str, description: str):
    if len(users) == 0:
        return ProjectCreateResult(status=StatusEnum.failed, message="No users provided")
    if len(id) == 0:
        return ProjectCreateResult(status=StatusEnum.failed)
    try:
        Processing.create_project(users, id, description)
    except:
        logging.error("Exception in project creation", exc_info=True)
        raise

    return ProjectCreateResult(status=StatusEnum.success)
