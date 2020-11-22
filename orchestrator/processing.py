from commons.lacmusDB.operation import image_processing
from commons.config import PROCESSING_BATCH_SIZE
from commons import minio
import logging
import requests


def check_new_images():
    images = image_processing.query_images_for_processing()
    if (images is not None) and len(images)>0:
        logging.info("new images arrived:\n %s"\
                     %['\t%s for %s, uploaded by %s\n'%(i.filename,str(i.project.id),i.user.nickname)\
                       for i in images])
    return images

def take_batch_for_processing(images):
    if len(images)<PROCESSING_BATCH_SIZE:
        image_to_process = images
    else:
        image_to_process = images[:PROCESSING_BATCH_SIZE]
    image_processing.mark_process_start(image_to_process)
    for image in image_to_process: # todo: create separate threads
        process_image(image)

def process_image(image):
    logging.info("processing image %s"%image.filename)
    file_object = minio.get_file(image.project_id,image.filename)
    logging.info("received %i data from minio "%len(file_object))
    data = {
        'image': (image.filename,file_object,'image/jpeg')
    }
    response = requests.post('http://127.0.0.1:5000/api/v0/infer',
                             files=data)
    objects=[]
    if 'objects' in response.json():
        objects = response.json()['objects']
    logging.info("got responce from model %s with objects %s"%(response,objects))
    image_processing.save_responce(image, objects)


