from fastapi import APIRouter
from api.v0.routes import ping
from api.v0.routes import user

router = APIRouter()

router.include_router(ping.router, tags=["ping"])
router.include_router(user.router, tags=["user"])
# router.include_router(predict.router, tags=["project"])