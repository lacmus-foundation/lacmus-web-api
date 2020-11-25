import threading
import requests
import logging
from commons.lacmusDB import db_definition
from commons.lacmusDB.operation import image_processing
from commons import minio


class ProcessingThread(threading.Thread):
    def __init__(self,image:db_definition.Image):
        threading.Thread.__init__(self)
        logging.info("creating processing thread for image %i:%s"%(image.id,image.filename))
        self.image = image

    def run(self):
        self.process_image()

    def process_image(self):
        image = self.image
        logging.info("processing image %s" % image.filename)
        file_object = minio.get_file(image.project_id, image.filename)
        logging.info("received %i data from minio " % len(file_object))
        data = {
            'image': (image.filename, file_object, 'image/jpeg')
        }
        response = requests.post('http://127.0.0.1:5000/api/v0/infer',
                                 files=data)
        objects = []
        if 'objects' in response.json():
            objects = response.json()['objects']
        logging.info("got responce from model %s with objects %s" % (response, objects))
        image_processing.save_responce(image, objects)
        logging.info("notify ftp api with image_id = %i" % image.id)
        try:
            response = requests.put('http://127.0.0.1:5001/api/v1/result',
                                    params={'image_id': image.id})  # todo: get ftp api/port from config
            if response.ok:
                logging.info("Got success response from ftp server")
            else:
                logging.error("Gor error from ftp server with code %i and message %s" %
                              (response.status_code, response.reason))
        except Exception:
            logging.error("Error calling ftp api", exc_info=True)