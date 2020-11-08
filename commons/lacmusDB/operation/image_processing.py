import datetime
from sqlalchemy.orm import joinedload

from commons.lacmusDB.db_definition import Image, ImageAnnotation
from commons.lacmusDB.db_definition import get_session


def create_file_entity(image:Image):
    s = get_session()
    s.add(image)
    s.commit()

def query_images_for_processing():
    s = get_session()
    images = s.query(Image).options(joinedload('annotation')).filter(ImageAnnotation.processing_start == None)
    return images.all()

def mark_process_start(images):
    s = get_session()
    for i in images:
        i.processing_start=datetime.now()
    s.add(images)
    s.commit()

