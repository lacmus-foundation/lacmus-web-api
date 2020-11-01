from fastapi import APIRouter, HTTPException, Request, Response
from commons.config import PROJECT_NAME, VERSION
from core.pong import Pong

router = APIRouter()

@router.get("/ping", response_model=Pong)
async def root() -> Pong:
    return Pong(pong=f"{PROJECT_NAME}, version {VERSION}")