from fastapi import FastAPI
from api.v0.routes.api import router as api_router
from core.config import API_PREFIX, DEBUG, PROJECT_NAME, VERSION
from lacmusDB import db_definition
import uvicorn


def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)
    application.include_router(api_router, prefix=API_PREFIX)
    db_definition.init_db()

    return application

app = get_application()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)