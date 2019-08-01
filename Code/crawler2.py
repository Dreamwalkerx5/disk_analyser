#  Copyright (c) 2019. Steven Taylor All rights reserved
import queue
import sys
import threading


def crawler_monitor(*args):
    comms = args[0]
    files_processed = args[1]
    gui = args[2]
    total_files = args[3]

    while total_files > files_processed:

        try:

            gui.progressBar.setValue(int((files_processed / total_files) * 100))

        except:

            print("Unexpected error:", sys.exc_info()[0])
            print(sys.exc_info()[1])

    print('Progress thread dying...')


class Crawler2(threading.Thread):

    def __init__(self, gui=None, total_files=0, root=None):
        super(Crawler2, self).__init__()

        self.gui = gui
        self.total_files = total_files
        self.root = root
        self.comms = queue.Queue
        self.files_processed = 0
        self.stop_request = threading.Event()
        self.crawler_monitor = None

    def run(self):
        # Start crawler monitor thread
        self.crawler_monitor = threading.Thread(target=crawler_monitor,
                                                args=(self.comms, self.files_processed, self.gui,
                                                      self.total_files,),
                                                daemon=True)
        self.crawler_monitor.start()

        self.crawl_directory(self.root)

    def join(self, timeout=None):
        self.stop_request.set()
        super(Crawler2, self).join(timeout)

    def crawl_directory(self, directory):
        # Check if thread has been told to stop
        if not self.stop_request.isSet():
            pass
