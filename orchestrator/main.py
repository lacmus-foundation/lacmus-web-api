import processing
import time
from commons import logging
import project_config


if __name__ == '__main__':
    logging.init_logging(project_config.PROJECT_SYMBOL)
    while(True):
        images = processing.check_new_images()
        if (images is not None) and len(images) > 0:
            processing.take_batch_for_processing(images)
        else:
            time.sleep(2)

