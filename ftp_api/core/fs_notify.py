from inotify.adapters import Inotify
from core import processing
import threading
import logging
import os

class NotifyThread(threading.Thread):
    def __init__(self,folder, project_id):
        threading.Thread.__init__(self)
        logging.info("creating notify thread for project %s in %s"%(project_id,folder))
        self.folder = folder
        self.project_id = project_id

    def run(self):
        logging.info("Running notify thread. First scan files from last run")
        for f in os.listdir(self.folder):
            if os.path.isfile(os.path.join(self.folder,f)):
                logging.info("File %s noticed unprocessed notify thread for project %s in %s"%(f,
                                                                                      self.project_id,self.folder))
                processing.Processing.process_incoming_file(self.folder,f,self.project_id)

        logging.info("Scan complete, start watching events")
        i = Inotify()
        i.add_watch(self.folder)

        for event in i.event_gen(yield_nones=False):
            (header, type_names, watch_path, filename) = event
            if ('IN_CLOSE_WRITE' in type_names):
                logging.info("File %s noticed by notify thread for project %s in %s"%(filename,
                                                                                      self.project_id,watch_path))
                processing.Processing.process_incoming_file(watch_path,filename,self.project_id)
