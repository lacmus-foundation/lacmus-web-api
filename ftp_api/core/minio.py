from minio import Minio
import os

from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)

def create_project(project_name:str):
    minioClient = Minio('localhost:9000',
                    access_key='qk1OtxQL54Cf',
                    secret_key='8VE9zlm1Z0mb')
    try:
           minioClient.make_bucket(project_name)
    except BucketAlreadyOwnedByYou as err:
           pass
    except BucketAlreadyExists as err:
           pass
    except ResponseError as err:
           raise

def upload_file(project_id:str, file_path:str, file_name: str):
    try:
        minioClient = Minio('localhost:9000',
                            access_key='qk1OtxQL54Cf',
                            secret_key='8VE9zlm1Z0mb')

        minioClient.fput_object(project_id, file_name, os.path.join(file_path,file_name))
    except ResponseError as err:
        print(err)