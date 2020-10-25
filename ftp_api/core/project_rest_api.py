from pydantic import BaseModel
from enum import auto
from fastapi_utils.enums import StrEnum
from typing import List
from core.ftp import FTPServer
from core import fs_notify
import threading



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

    ftp_dir = FTPServer.create_project(users,id,description)
    th = fs_notify.NotifyThread(ftp_dir)
    th.setDaemon(False)
    th.start()
    return ProjectCreateResult(status=StatusEnum.success)