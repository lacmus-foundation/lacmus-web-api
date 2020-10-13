from fastapi import APIRouter, HTTPException, File, UploadFile
from core.config import PROJECT_NAME, VERSION
from core.models import predict_result
from core.models import job_result
from core.models import s3

router = APIRouter()

@router.post("/predict/on_image", response_model=job_result.Job)
async def predict_on_image(image: UploadFile = File(...)) -> job_result.Job:
    job = job_result.Job()
    job.job = job_result.JobID('{12345678-1234-5678-1234-567812345678}')
    return job

@router.post("/predict/on_s3", response_model=job_result.JobArray)
async def predict_on_s3(res: s3.Predict) -> job_result.JobArray:
    job_arr = job_result.JobArray()
    job_arr.jobs = []
    job_arr.jobs.append(job_result.JobID('{12345678-1234-5678-1234-567812345678}'))
    return job_arr

@router.get("/predict/result/{job}", response_model=predict_result.Result)
async def get_result(job: str) -> predict_result.Result:
    result = predict_result.Result()
    result.status = predict_result.StatusEnum.finished
    result.objects = []
    obj = predict_result.Object()
    obj.label = "person"
    obj.xmax = 100
    obj.xmin = 80
    obj.ymax = 200
    obj.ymin = 170
    result.objects.append(obj)

    return result