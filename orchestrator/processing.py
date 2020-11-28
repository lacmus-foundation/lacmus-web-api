import time
import logging
import queue
from commons.lacmusDB.operation import image_processing
from commons.config import ITEMS_IN_QUEUE_FOR_NEW_ML_WORKER, MAX_ML_WORKERS_COUNT
import processing_thread
import openstack_cmds


class Processing:
    def __init__(self):
        # It could be the case, workers are there and running, but not in workers[]
        # due to application crush, so we need to pick up those one during startup (also it simplifies debug)
        self.avail_workers = queue.Queue()
        for worker in openstack_cmds.try_to_find_exising_workers():
            self.avail_workers.put(worker)
        self.processing_threads = []
        self.image_queue = queue.Queue()

    def clean_empty_threads(self):
        new_threads = []
        for old_thread in self.processing_threads:
            if old_thread.is_alive():
                new_threads.append(old_thread)
        logging.info("Cleaning threads. Was %i, become %i" % (len(self.processing_threads), len(new_threads)))
        self.processing_threads = new_threads

    def run(self):
        while True:
            images = self.check_new_images()
            self.clean_empty_threads()
            if (images is not None) and len(images) > 0:
                for image in images:
                    self.image_queue.put(image)
                if len(self.processing_threads) == 0:
                    self.create_new_thread()
                if len(self.processing_threads) < MAX_ML_WORKERS_COUNT \
                        and self.image_queue.qsize() > ITEMS_IN_QUEUE_FOR_NEW_ML_WORKER:
                    self.create_new_thread()
            else:
                time.sleep(10)
                self.clean_empty_threads()

    def create_new_thread(self):
        avail_worker = None
        try:
            avail_worker = self.avail_workers.get(block=False)
            logging.info("There are old workers, passing one to thread")
        except queue.Empty:
            logging.info("No workers available, passing None")
        th = processing_thread.ProcessingThread(self.image_queue, avail_worker)
        self.processing_threads.append(th)
        th.start()

    def check_new_images(self):
        images = image_processing.query_images_for_processing()
        if (images is not None) and len(images) > 0:
            logging.info("new images arrived:\n %s" \
                         % "\n".join(["\t%s for %s, uploaded by %s" % (i.filename, str(i.project.id), i.user.nickname) \
                                      for i in images]))
            image_processing.mark_process_start(images)
        return images
