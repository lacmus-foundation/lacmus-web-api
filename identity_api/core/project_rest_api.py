from pydantic import BaseModel
from enum import auto
from fastapi_utils.enums import StrEnum
from typing import List
from commons.lacmusDB.db_definition import Project
from commons.lacmusDB.operation.users_projects import create_project_entity
import commons.config as config
import uuid
import requests
import logging

class StatusEnum(StrEnum):
    success = auto()
    failed = auto()

class ProjectCreateResult(BaseModel):
    id: str=""
    status: StatusEnum
    message: str=""

def createProject(users:List[str],description:str):
    logging.info("Create project request received for users: %s"%(','.join(users)))
    if len(users)==0:
        return ProjectCreateResult(status=StatusEnum.failed, message="You should provide some users")
    project_uuid = uuid.uuid1()
    new_project = Project(uuid=project_uuid,description=description)
    # uuid is too long to create linux group based on it, so for FTP we have to generate shorter id
    project_id = create_project_entity(new_project, users)
    if (project_id!=-1):
        ftp_result = requests.post('http://%s:%i/api/v1/project'%(config.FTP_SERVER,config.FTP_API_PORT),
                               params={'users': users, 'description':description, 'id': str(project_id)})
        logging.info("FTP returned %s with reason %s" % (ftp_result.status_code, ftp_result.reason))
        if ftp_result.status_code!=200:
            return ProjectCreateResult(status=StatusEnum.failed, message = 'Failed to create project on FTP')
    else:
        return ProjectCreateResult(status=StatusEnum.failed, message = 'Failed to create project in DB')
    return ProjectCreateResult(status=StatusEnum.success,id=str(project_uuid))