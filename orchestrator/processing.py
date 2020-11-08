from commons.lacmusDB.operation.image_processing import query_images_for_processing, mark_process_start
from commons.config import PROCESSING_BATCH_SIZE


def check_new_images():
    images = query_images_for_processing()
    print(images)
    return images

def take_batch_for_processing(images):
    if len(images)<PROCESSING_BATCH_SIZE:
        image_to_process = images
    else:
        image_to_process = images[:PROCESSING_BATCH_SIZE]
    mark_process_start(image_to_process)

