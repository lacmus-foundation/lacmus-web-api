from fastapi import FastAPI, HTTPException, Response
from models import view_models

app = FastAPI(openapi_url="/api/v1/predict/openapi.json")

@app.get('/api/v1/predict/probe', 
    status_code=200)
async def probe():
    return {'staus': 'workong'}

@app.post('/api/v1/predict/push/{model_type}', 
    status_code=201, 
    response_model=view_models.Tasks,
    responses={
        404: {"model": view_models.Error, "description": "files is empty or wrong"},
        500: {"model": view_models.Error, "description": "internal server error"}})
async def push(files: view_models.Files):
    if len(files.files) < 1:
        raise HTTPException(422, detail='no input files')
    
    tasks = view_models.Tasks()
    for i in range(0, len(files.files)):
        tasks.tasks.append(f'fake_task{i}')
    return tasks

@app.get('/api/v1/predict/pop/{model_type}/{task_id}',
    response_model=view_models.TaskResult,
    responses={
        404: {"model": view_models.Error, "description": "task is not found"},
        500: {"model": view_models.Error, "description": "internal server error"}})
async def pop():
    return view_models.TaskResult()