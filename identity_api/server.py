from fastapi import FastAPI
from api.v0.routes.api import router as api_router
from commons.config import API_PREFIX, DEBUG
from commons.lacmusDB import db_definition
from core import project_config
from commons import logging
import uvicorn


def get_application() -> FastAPI:
    logging.init_logging(project_config.PROJECT_SYMBOL)
    db_definition.init_db()
    application = FastAPI(title=project_config.PROJECT_NAME, debug=DEBUG, version=project_config.VERSION)
    application.include_router(api_router, prefix=API_PREFIX)

    return application

app = get_application()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5002)