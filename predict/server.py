from fastapi import FastAPI, HTTPException, Response
from models import view_models

app = FastAPI()

@app.post('api/v1/push/{model_type}', 
    status_code=201, 
    response_model=view_models.TaskResult,
    responses={
        404: {"model": view_models.Error, "description": "files is empty or wrong"},
        500: {"model": view_models.Error, "description": "internal server error"}})
async def push(files: view_models.Files, response: Response):
    if len(files.files) < 1:
        raise HTTPException(422, detail='no input files')
    return view_models.Tasks()

@app.get('api/v1/pop/{task_id}',
    response_model=view_models.TaskResult,
    responses={
        404: {"model": view_models.Error, "description": "task is not found"},
        500: {"model": view_models.Error, "description": "internal server error"}})
async def pop():
    return view_models.TaskResult()