from pydantic import BaseModel
from enum import auto
from fastapi_utils.enums import StrEnum
from typing import List
from core.ftp import FTPServer

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
    id: str="" # there is no reason to return id from ftp API added for unification with Identity API
    status: StatusEnum

def createUser(login:str, password:str, roles:UserRoles):
    if password=="":
        return UserCreateResult(status=StatusEnum.failed)
    if len(roles)==0:
        return UserCreateResult(status=StatusEnum.failed)

    FTPServer.create_user(login,password)
    return UserCreateResult(status=StatusEnum.success)