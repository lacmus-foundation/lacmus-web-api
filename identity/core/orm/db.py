from fastapi_utils.session import FastAPISessionMaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from core.config import get_config
from functools import lru_cache

Base = declarative_base()

@lru_cache()
def get_fastapi_sessionmaker() -> FastAPISessionMaker:
    user = get_config().db_user
    password = get_config().db_password
    host = get_config().db_host
    database = get_config().db_name
    port = get_config().db_port
    database_uri = f'postgresql://{user}:{password}@{host}:{port}/{database}'
    
    return FastAPISessionMaker(database_uri)