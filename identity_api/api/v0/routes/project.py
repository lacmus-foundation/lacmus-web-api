from fastapi import APIRouter, Query
from core.project_rest_api import createProject, ProjectCreateResult
from typing import List


router = APIRouter()

@router.post("/project", response_model=ProjectCreateResult)
async def root(users:List[str]=Query(None),
               description:str="" ) -> ProjectCreateResult :
    return createProject(users,description)