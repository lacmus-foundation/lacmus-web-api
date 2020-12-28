from fastapi import APIRouter, Query
from core.user_rest_api import createUser
from core.user_rest_api import UserCreateResult
from typing import List
from core.user_rest_api import UserRoles


router = APIRouter()

@router.post("/user", response_model=UserCreateResult)
async def root(nick_name:str,password:str, roles:List[str]=Query(None) ) -> UserCreateResult:
    return createUser(nick_name,password,UserRoles(roles))