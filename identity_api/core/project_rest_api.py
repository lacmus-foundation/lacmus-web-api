from pydantic import BaseModel
from enum import auto
from fastapi_utils.enums import StrEnum
from typing import List
from commons.lacmusDB.db_definition import Project, User, create_project_entity
import uuid
import requests

class StatusEnum(StrEnum):
    success = auto()
    failed = auto()

class ProjectCreateResult(BaseModel):
    id: str="";
    status: StatusEnum
    message: str="";

def createProject(users:List[str],description:str):
    if len(users)==0:
        return ProjectCreateResult(status=StatusEnum.failed, message="You should provide some users")
    project_uuid = uuid.uuid1()
    #todo: check user actually exists
    new_project = Project(uuid=project_uuid,description=description)
    # uuid is too long to create linux group based on it, so for FTP we have to generate shorter id
    project_id = create_project_entity(new_project, users)
    if (project_id!=-1):
        ftp_result = requests.post('http://127.0.0.1:5001/api/v1/project',
                               params={'users': users, 'description':description, 'id': 'project'+str(project_id)})
        #todo: check result
    else:
        return ProjectCreateResult(status=StatusEnum.failed, message = 'Failed to create project in DB')
    return ProjectCreateResult(status=StatusEnum.success,id=str(uuid))