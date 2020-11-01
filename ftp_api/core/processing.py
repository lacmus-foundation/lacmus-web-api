from commons.lacmusDB.db_definition import Image, create_file_entity
from core import fs_notify

from core import minio
from core.ftp import FTPServer


class Processing():
    @staticmethod
    def process_incoming_file(path:str, file_name:str, project_id:str):
        # check file in valid image
        # if not - move to errors
        # if yes - upload to s3, create record in DB, delete, create label in in_process
        minio.upload_file(project_id,path,file_name)
        new_image = Image(filename=file_name)
        create_file_entity(new_image)


        return

    @staticmethod
    def create_project(users:str, id:str, description:str):
        ftp_dir = FTPServer.create_project(users, id, description)
        minio.create_project(id)
        th = fs_notify.NotifyThread(ftp_dir, id)
        th.setDaemon(False)
        th.start()
        return