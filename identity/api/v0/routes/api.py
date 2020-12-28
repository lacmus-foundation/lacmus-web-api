from fastapi import APIRouter
from api.v0.routes import ping

router = APIRouter()

router.include_router(ping.router, tags=["ping"])