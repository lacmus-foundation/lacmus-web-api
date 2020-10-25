from inotify.adapters import Inotify
from core.processing import Processing
import threading
import os


class NotifyThread(threading.Thread):
    def __init__(self,folder):
        threading.Thread.__init__(self)
        self.folder = folder
        print ("NotifyThread init for %s"%folder)

    def run(self):
        print ("NotifyThread start")
        i = Inotify()
        i.add_watch(self.folder)

        for event in i.event_gen(yield_nones=False):
            (header, type_names, watch_path, filename) = event
            if ('IN_CLOSE_WRITE' in type_names):
                Processing.process_incoming_file(os.path.join(watch_path,filename))
        print ("NotifyThread end :/")