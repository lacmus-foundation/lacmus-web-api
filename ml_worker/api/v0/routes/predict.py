from fastapi import APIRouter, HTTPException, File, UploadFile
from core.models import predict
from core.models import cv_models

router = APIRouter()

@router.post("/infer/{model_name}", response_model=predict.Result)
async def predict_on_image(model_name: cv_models.ModelEnum, image: UploadFile = File(...)) -> predict.Result:
    
    
    result = predict.Result(
        objects= []
    )
    result.objects = []
    obj = predict.Object(
        label = "person",
        xmax = 100,
        xmin = 80,
        ymax = 200,
        ymin = 170
    )
    result.objects.append(obj)
    return result