from fastapi import APIRouter, Query
from core.user_rest_api import createUser,queryUser, UserCreateResult, UserQueryResult
from typing import List
from core.user_rest_api import UserRoles


router = APIRouter()

@router.post("/user", response_model=UserCreateResult)
async def root(nick_name:str,password:str, roles:List[str]=Query(None),
               first_name:str="",last_name:str="",
               middle_name:str="", email:str="", description:str="") -> UserCreateResult:
    return createUser(nick_name,password, roles,
               first_name,last_name,middle_name, email,description)

@router.get("/user", response_model=UserQueryResult)
async def root(id:str)->UserQueryResult:
    return queryUser(id)