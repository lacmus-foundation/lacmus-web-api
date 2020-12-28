from fastapi import APIRouter
from commons.api import ping
from api.v0.routes import user
from api.v0.routes import project
from api.v0.routes import result

router = APIRouter()

router.include_router(ping.router, tags=["ping"])
router.include_router(user.router, tags=["user"])
router.include_router(project.router, tags=["project"])
router.include_router(result.router, tags=["result"])
