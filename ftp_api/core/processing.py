from commons.lacmusDB.db_definition import Image
from commons.lacmusDB.operation.image_processing import create_file_entity
from core import fs_notify

from core import minio
from core.ftp import FTPServer


class Processing():
    @staticmethod
    def process_incoming_file(path:str, file_name:str, project_id:str):
        # todo: check file is valid image (if not - move to errors)
        # todo: remove file from ftp
        # todo - properly identify user and project for file
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

    @staticmethod
    def init_listeneres():
        # todo - load project lists from DB and create inotify for all active ones
        return