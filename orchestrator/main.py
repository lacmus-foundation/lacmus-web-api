import processing
import time

if __name__ == '__main__':
    while(True):
        images = processing.check_new_images()
        if len(images)>0:
            processing.take_batch_for_processing(images)
        else:
            time.sleep(2)

