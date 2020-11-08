from fastapi import APIRouter
from commons.api.pong import Pong
from core import project_config

router = APIRouter()

@router.get("/ping", response_model=Pong)
async def root() -> Pong:
    return Pong(pong=f"{project_config.PROJECT_NAME}, version {project_config.VERSION}")