from pydantic import BaseModel
from enum import auto
from fastapi_utils.enums import StrEnum
from typing import List
from commons.lacmusDB.db_definition import User
from commons.lacmusDB.operation.users_projects import create_user_entity, check_user_exists
import commons.config as config
import uuid
import requests
import logging

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
    # todo - check roles provided really exists (technicaly done in DB function, just not passes it back to API)
    # todo - other fields validation
    user_uuid = str(uuid.uuid1())
    logging.info("got user creation request, creating user %s with id %s"%(nick_name,user_uuid))
    existing_user = check_user_exists(nick_name)
    out_message = ""
    if (len(existing_user)>0):
        logging.warning("user %s already exists in DB with id %s. Shouldn't happen on prod, but fine for debug"%(nick_name,existing_user[0].uuid))
        user_uuid = existing_user[0].uuid
        out_message = "user was existing, parameters not set"
    else:
        new_user = User(uuid=user_uuid,nickname=nick_name, firstname=first_name,
                    lastname=last_name, middlename=middle_name, email=email,
                    description=description)
        try:
            create_user_entity(new_user,roles)
        except Exception as ex:
            logging.error("Error creating user in DB",exc_info=True)
            if type(ex)==ValueError:
                return UserCreateResult(status=StatusEnum.failed, message='Error creating user in DB -%s'%ex.args[0])
            else:
                return UserCreateResult(status=StatusEnum.failed, message='Error creating user in DB')
    logging.info("User created in DB, creating it on FTP")
    # todo pass server address as parameter
    try:
        ftp_result = requests.post('http://%s:%i/api/v1/user'%(config.FTP_SERVER,config.FTP_API_PORT),
                  params={'nick_name':nick_name, 'password':password, 'roles':roles })
        logging.info("FTP returned %s with reason %s"%(ftp_result.status_code,ftp_result.reason))
        if (ftp_result.status_code!=200):
            return UserCreateResult(status=StatusEnum.failed, message = 'Error creating user on ftp')
    except Exception as ex:
        logging.error("Error creating user at ftp",exc_info=True)
        return UserCreateResult(status=StatusEnum.failed, message='Error creating user on ftp')
    return UserCreateResult(id=user_uuid, status=StatusEnum.success, message=out_message)

def queryUser(id:str):
    # todo - implement
    return UserQueryResult()

def deleteUser(id:str):
    # todo - implement
    return UserDeleteResult()

def listUsers(page:int, count:int):
    # todo - implement
    return UserListResult()