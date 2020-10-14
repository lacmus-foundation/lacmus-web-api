from fastapi import APIRouter, HTTPException, File, UploadFile
from core.api_models.common import Object, Result, ModelEnum

router = APIRouter()

@router.post("/infer/{model_name}", response_model=Result)
async def predict_on_image(model_name: ModelEnum, image: UploadFile = File(...)) -> Result:
    result = Result(
        objects= []
    )
    result.objects = []
    obj = Object(
        label = "person",
        xmax = 100,
        xmin = 80,
        ymax = 200,
        ymin = 170
    )
    result.objects.append(obj)
    return result