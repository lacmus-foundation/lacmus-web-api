from fastapi import FastAPI
from api.v0.routes.api import router as api_router
from core.config import API_PREFIX, DEBUG, PROJECT_NAME, VERSION

def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)
    
    application.include_router(api_router, prefix=API_PREFIX)
    
    return application

app = get_application()