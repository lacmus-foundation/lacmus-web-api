from pydantic import BaseModel
from enum import auto
from fastapi_utils.enums import StrEnum
from typing import List
from commons.lacmusDB.db_definition import User
from commons.lacmusDB.operation.users_projects import create_user_entity
import uuid
import requests

class StatusEnum(StrEnum):
    success = auto()
    failed = auto()

class Roles(StrEnum):
    admin = auto()
    user = auto()

class UserRoles(List[Roles]):
    def __init__(self,strRoles:List[str]):
        self.append([Roles(o) for o in strRoles])


class UserCreateResult(BaseModel):
    id: str=""
    status: StatusEnum
    message: str=""

class UserQueryResult(BaseModel):
    nick_name: str
    first_name: str
    middle_name: str
    last_name: str
    roles: List[str]
    projects: List[str]
    email: str

class UserListResult(BaseModel):
    max_page: int
    users: List[str]

class UserDeleteResult(BaseModel):
    result: str

def createUser(nick_name:str,password:str, roles:List[str],
               first_name:str,last_name:str,
               middle_name, email:str,description:str):
    if len(password)<4:
        return UserCreateResult(status=StatusEnum.failed, message = "password cann't be less then 4 chars")
    if len(roles)==0:
        return UserCreateResult(status=StatusEnum.failed, message = "at least one role to be provided")
    # todo - check roles provided really exists
    # todo - other fields validation
    user_uuid = uuid.uuid1()
    new_user = User(uuid=user_uuid,nickname=nick_name, firstname=first_name,
                    lastname=last_name, middlename=middle_name, email=email,
                    description=description
                    )
    create_user_entity(new_user,roles)
    # todo pass server address as parameter
    ftp_result = requests.post('http://127.0.0.1:5001/api/v1/user',
                  params={'nick_name':nick_name, 'password':password, 'roles':roles })
    # todo - error handling

    return UserCreateResult(id=str(user_uuid), status=StatusEnum.success)

def queryUser(id:str):
    # todo - implement
    return UserQueryResult()

def deleteUser(id:str):
    # todo - implement
    return UserDeleteResult()

def listUsers(page:int, count:int):
    # todo - implement
    return UserListResult()