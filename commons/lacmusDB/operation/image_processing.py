from datetime import datetime
import logging
from sqlalchemy.orm import joinedload
from commons.lacmusDB import db_definition


def create_file_entity(image: db_definition.Image, project_id: str, user_login: str):
    s = db_definition.get_session()
    project = s.query(db_definition.Project).filter(db_definition.Project.id == int(project_id)).first()
    if (project is None):
        logging.error("Cann't determine project for id %s" % project_id)
        raise
    image.project = project
    user = s.query(db_definition.User).filter(db_definition.User.nickname == user_login).first()
    if (user is None):
        logging.error("Cann't determine user for login %s" % user_login)
        raise
    image.user = user
    s.add(image)
    s.commit()


def query_images_for_processing():
    try:
        logging.info("Getting images for processing list from DB")
        s = db_definition.get_session()
        images = s.query(db_definition.Image).options( \
            joinedload(db_definition.Image.user), joinedload(db_definition.Image.project)). \
            filter(db_definition.Image.processing_start == None).all()
        s.close()
        return images
    except Exception as e:
        logging.error("Exception while getting projects", exc_info=True)


def mark_process_start(images):
    s = db_definition.get_session()
    for i in images:  # todo - one query "in"
        db_image = s.query(db_definition.Image).filter(db_definition.Image.id == i.id).first()
        db_image.processing_start = datetime.now()
        s.add(db_image)
    s.commit()
    s.close()


def save_responce(image, objects):
    try:
        s = db_definition.get_session()
        db_image = s.query(db_definition.Image).filter(db_definition.Image.id == image.id).first()
        for raw_obj in objects:
            object = db_definition.ImageObjects(x_min=raw_obj['xmin'], x_max=raw_obj['xmax'],
                                                y_min=raw_obj['ymin'], y_max=raw_obj['ymax'],
                                                class_label=raw_obj['label'], class_number=0)
            db_image.objects.append(object)
        db_image.processing_end = datetime.now()
        s.add(db_image)
        s.commit()
        s.close()
        logging.info('Saved object successfully')
    except Exception as e:
        logging.error("Exception while saving projessing results projects", exc_info=True)


def query_single_image(image_id) -> db_definition.Image:
    try:
        logging.info("Getting image with ID %i from DB" % image_id)
        s = db_definition.get_session()
        image = s.query(db_definition.Image).options(
            joinedload(db_definition.Image.user), joinedload(db_definition.Image.project),
            joinedload(db_definition.Image.objects)). \
            filter(db_definition.Image.id == image_id).first()
        s.close()
        return image
    except Exception as e:
        logging.error("Exception while getting projects", exc_info=True)
