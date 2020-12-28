from inotify.adapters import Inotify
from core import processing
import threading
import logging

class NotifyThread(threading.Thread):
    def __init__(self,folder, project_id):
        threading.Thread.__init__(self)
        logging.info("creating notify thread for project %s in %s"%(project_id,folder))
        self.folder = folder
        self.project_id = project_id

    def run(self):
        i = Inotify()
        i.add_watch(self.folder)

        for event in i.event_gen(yield_nones=False):
            (header, type_names, watch_path, filename) = event
            if ('IN_CLOSE_WRITE' in type_names):
                logging.info("File %s noticed by notify thread for project %s in %s"%(filename,
                                                                                      self.project_id,watch_path))
                processing.Processing.process_incoming_file(watch_path,filename,self.project_id)
