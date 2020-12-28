from minio import Minio
import os
from commons import config
import logging

from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)

def bucket_name(id:str): return  'project%s'%id

def get_client():
    return Minio('localhost:9000',
                            access_key=config.MINIO_ACCESS_KEY,
                            secret_key=config.MINIO_SECRET_KEY,
                            secure=False)

def create_project(project_id:str):
    try:
        logging.info("Creating on minio project %s"%bucket_name(project_id))
        minioClient = get_client()
        minioClient.make_bucket(bucket_name(project_id))
    except BucketAlreadyOwnedByYou as err:
        logging.warning("minio returned error BucketAlreadyOwnedByYou, but it's fine")
        pass
    except BucketAlreadyExists as err:
        logging.warning("minio returned error BucketAlreadyExists, but it's fine")
        pass
    except ResponseError as err:
        logging.error("Cann't create minio bucket for project",exc_info=True)
        raise err

def upload_file(project_id:str, file_path:str, file_name: str):
    try:
        minioClient = get_client()
        minioClient.fput_object(bucket_name(project_id), file_name, os.path.join(file_path,file_name))
    except:
        logging.error("Cann't upload file %s in bucket %s from minio"%(os.path.join(file_path,file_name),project_id),
                      exc_info=True)

def get_file(project_id:str, file_name: str):
    try:
        minioClient = get_client()
        response = minioClient.get_object(bucket_name(project_id),file_name)
        return response.data
    except:
        logging.error("Cann't get file %s in bucket %s from minio"%(file_name,project_id),exc_info=True)
    finally:
        response.close()
        response.release_conn()

def download_to_file(project_id:str, source_file_name:str,target_file:str):
    try:
        logging.info("downloading file %s to %s for project %s"%(source_file_name,target_file,project_id))
        minioClient = get_client()
        minioClient.fget_object(bucket_name(project_id), source_file_name, target_file)
    except:
        logging.error("Cann't download file %s in bucket %s from minio to %s"%(source_file_name,project_id,target_file),
                      exc_info=True)