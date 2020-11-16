import datetime
import logging
from sqlalchemy.orm import joinedload
from commons.lacmusDB import db_definition


def create_file_entity(image:db_definition.Image, project_id: str, user_login:str):
    s = db_definition.get_session()
    project = s.query(db_definition.Project).filter(db_definition.Project.id == int(project_id)).first()
    if (project is None):
        logging.error("Cann't determine project for id %s"%project_id)
        raise
    image.project=project
    user = s.query(db_definition.User).filter(db_definition.User.nickname == user_login).first()
    if (user is None):
        logging.error("Cann't determine user for login %s"%user_login)
        raise
    image.user=user
    s.add(image)
    s.commit()

def query_images_for_processing():
    s = db_definition.get_session()
    images = s.query(db_definition.Image).options(joinedload('annotation')).\
        filter(db_definition.ImageAnnotation.processing_start == None)
    return images.all()

def mark_process_start(images):
    s = db_definition.get_session()
    for i in images:
        i.processing_start=datetime.now()
    s.add(images)
    s.commit()

