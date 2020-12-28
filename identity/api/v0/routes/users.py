from fastapi import APIRouter, HTTPException, Request, Response
from core.api_models.common import Pong
from typing import List

router = APIRouter()

@router.get("/users", response_model=List[User])
async def get_users(page: int = 0, size: int = 50, db: Session = Depends(get_db)):
    db_msgs = await db_controller.get_records(db=db, skip=page*size, limit=size)
    records = []
    for msg in db_msgs:
        records.append(record.Record().create_from_db(msg))
        
    return records