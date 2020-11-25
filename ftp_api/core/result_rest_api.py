from pydantic import BaseModel
from enum import auto
from fastapi_utils.enums import StrEnum
from core.processing import Processing
import logging


class StatusEnum(StrEnum):
    success = auto()
    failed = auto()


class ResultPublishReply(BaseModel):
    status: StatusEnum
    message = ""


def publishResult(image_id: int):
    try:
        Processing.publish_processing_result(image_id)
    except Exception:
        logging.error("Exception in project creation", exc_info=True)
        raise

    return ResultPublishReply(status=StatusEnum.success)
