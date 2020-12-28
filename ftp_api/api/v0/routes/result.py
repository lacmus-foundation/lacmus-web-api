from fastapi import APIRouter, Query
from core.result_rest_api import publishResult
from core.result_rest_api import ResultPublishReply

router = APIRouter()


@router.put("/result", response_model=ResultPublishReply)
async def root(image_id: int) -> ResultPublishReply:
    return publishResult(image_id)
