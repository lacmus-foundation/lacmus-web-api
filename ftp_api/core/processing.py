import logging
import os
from PIL import Image
from commons.lacmusDB import db_definition
from commons.lacmusDB.operation.image_processing import create_file_entity
from commons.lacmusDB.operation.users_projects import get_active_projects
from core import fs_notify
from commons import minio
from core.ftp import FTPServer


class Processing():
    @staticmethod
    def process_incoming_file(path: str, file_name: str, project_id: str):
        try:
            logging.info("verifying file %s in %s" % (file_name, path))
            im = Image.open(os.path.join(path, file_name))
            im.verify()
        except Exception as ex:
            logging.error("Exception while verifying file %s in %s" % (file_name, path), exc_info=True)
            logging.info("moving file to error")
            FTPServer.move_file_to_error(path, file_name)
            return
            # No need to re-raise exception, otherwise we'll kill monitoring thread on every invalid file
        try:
            logging.info("uploading file %s in %s" % (file_name, path))
            minio.upload_file(project_id, path, file_name)
        except Exception as ex:
            logging.error("Cann't upload file to minio", exc_info=True)
            return
        user_id = FTPServer.get_user_login(path,file_name)
        logging.info("Collected user_id %s for file %s. Creating record in DB"%(user_id,file_name))
        try:
            new_image = db_definition.Image(filename=file_name)
            create_file_entity(new_image,project_id,user_id)
        except Exception as ex:
            logging.error("Cann't create DB entity for file %s"%file_name, exc_info=True)
            return
        FTPServer.remove_file(path,file_name)
        return

    @staticmethod
    def start_thread(ftp_dir, id):
        th = fs_notify.NotifyThread(ftp_dir, id)
        th.setDaemon(False)
        th.start()

    @staticmethod
    def create_project(users: str, id: str, description: str):
        ftp_dir = FTPServer.create_project(users, id, description)
        minio.create_project(id)
        Processing.start_thread(ftp_dir, id)
        return

    @staticmethod
    def init_listeners():
        projects = get_active_projects()
        for p in projects:
            Processing.start_thread(FTPServer.get_project_path(p.id), p.id)
