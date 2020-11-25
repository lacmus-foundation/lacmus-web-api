import logging
from commons.lacmusDB.operation import image_processing
from commons.config import PROCESSING_BATCH_SIZE
import processing_thread


def check_new_images():
    images = image_processing.query_images_for_processing()
    if (images is not None) and len(images) > 0:
        logging.info("new images arrived:\n %s" \
                     % ['\t%s for %s, uploaded by %s\n' % (i.filename, str(i.project.id), i.user.nickname) \
                        for i in images])
    return images


def take_batch_for_processing(images):
    if len(images) < PROCESSING_BATCH_SIZE:
        image_to_process = images
    else:
        image_to_process = images[:PROCESSING_BATCH_SIZE]
    image_processing.mark_process_start(image_to_process)
    threads = []
    for image in image_to_process:
        #todo: it will be better to give all available images to threads, splitting them in batches, to avoid
        #one thread waiting for others?
        th = processing_thread.ProcessingThread(image)
        th.start()
        threads.append(th)
    for th in threads:
        th.join()
