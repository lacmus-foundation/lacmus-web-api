import threading
import requests
import logging
import queue
import time
import openstack_cmds
from commons.lacmusDB.operation import image_processing
from commons import minio
from commons.config import KILL_WORKER_AFTER, ML_WORKER_PORT
from ml_worker import MLWorker


class ProcessingThread(threading.Thread):
    def __init__(self, processing_queue: queue.Queue, worker: MLWorker):
        threading.Thread.__init__(self)
        logging.info("creating processing thread for, current queue len is %i" % processing_queue.qsize())
        self.processing_queue = processing_queue
        self.worker = worker

    def run(self):
        self.process_queue()

    def process_queue(self):
        logging.info("Starting processing thread")
        if self.worker is None:
            worker = openstack_cmds.create_ml_worker()
            if worker is None:
                logging.error("Failed to create worker, can't process anything will try later")
                time.sleep(60)  # avoid flooding openstack, if it's not working anyway
                return
            self.worker = worker
        else:
            logging.info("Reusing existing worker %s with IP %s "%(self.worker.server['name'], self.worker.ip))
        empty_cycles = 0
        while True:
            try:
                image = self.processing_queue.get(block=False)
                logging.info("Thread: Got image %s for project %i from queue. %i images left  " %
                             (image.filename, image.project_id,self.processing_queue.qsize()))
                self.process_image(image)
                empty_cycles = 0
            except queue.Empty:
                logging.info("Thread: Queue is empty for %i seconds " % empty_cycles)
                time.sleep(1)
                empty_cycles += 1
                if empty_cycles > KILL_WORKER_AFTER:
                    logging.info("Queue is empty of more then %i seconds. Finishing" % KILL_WORKER_AFTER)
                    openstack_cmds.kill_worker(self.worker)
                    return

    def process_image(self, image):
        logging.info("processing image %s" % image.filename)
        try:
            file_object = minio.get_file(image.project_id, image.filename)
            logging.info("received %i data from minio " % len(file_object))
            data = {
                'image': (image.filename, file_object, 'image/jpeg')
            }
            response = requests.post('http://%s:%i/api/v2/infer' % (self.worker.ip, ML_WORKER_PORT),
                                     files=data)
            objects = []
            if 'objects' in response.json():
                objects = response.json()['objects']
            logging.info("got response from model %s with objects %s" % (response, objects))
            image_processing.save_responce(image, objects)
            logging.info("notify ftp api with image_id = %i" % image.id)
        except Exception:
            logging.error("Error processing image", exc_info=True)
            # todo - probably we have to mark image as errorneous in DB and publish to errors on ftp?
            # or try to reprocess it later
        try:
            response = requests.put('http://127.0.0.1:5001/api/v1/result',
                                    params={'image_id': image.id})  # todo: get ftp api ip:port from config
            if response.ok:
                logging.info("Got success response from ftp server")
            else:
                logging.error("Gor error from ftp server with code %i and message %s" %
                              (response.status_code, response.reason))
        except Exception:
            logging.error("Error calling ftp api", exc_info=True)
