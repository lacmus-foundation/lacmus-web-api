from fastapi import APIRouter
from api.v0.routes import user
from api.v0.routes import project

router = APIRouter()

router.include_router(user.router, tags=["user"])
router.include_router(project.router, tags=["project"])