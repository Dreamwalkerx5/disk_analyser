#  Copyright (c) 2019. Steven Taylor All rights reserved
import queue
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

from Code.database import Record
from Code.database import Database


def crawler_monitor(*args):
    parent = args[0]
    gui = args[1]
    total_files = args[2]

    while parent.total_files > parent.files_processed:

        try:

            gui.update_progress_bar(int((parent.files_processed / parent.total_files) * 100))
            time.sleep(0.1)

        except:

            print("Unexpected error:", sys.exc_info()[0])
            print(sys.exc_info()[1])

    print('Progress thread dying...')


class Crawler2(threading.Thread):
    files_processed: int

    def __init__(self, parent=None, gui=None, total_files=0, root=None, parent_id=0):
        super(Crawler2, self).__init__()

        self.parent = parent
        self.gui = gui
        self.total_files = total_files
        self.root = root
        self.parent_id = parent_id
        self.files_processed = 0
        self.stop_request = threading.Event()
        self.crawler_monitor = None

    def run(self):
        try:
            # Start crawler monitor thread
            self.crawler_monitor = threading.Thread(target=crawler_monitor,
                                                    args=(self, self.parent,
                                                          self.total_files,),
                                                    daemon=True)
            self.crawler_monitor.start()

            self.gui.info_label.setText('Crawling disk...')
            self.crawl_directory(self.root, self.parent_id)
            self.gui.info_label.setText('Finished disk crawl.')

            # Update view
            self.parent.create_view()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            print(sys.exc_info()[1])

    def join(self, timeout=None):
        self.stop_request.set()
        super(Crawler2, self).join(timeout)

    def crawl_directory(self, directory, parent_id):
        print('New directory...')
        try:
            # Check if thread has been told to stop
            if not self.stop_request.isSet():
                database = Database(self.gui)
                entries = Path(directory)
                for entry in entries.iterdir():

                    name = entry.name
                    info = entry.stat()
                    if entry.is_dir():

                        directory_flag = True

                    else:

                        directory_flag = False

                    file_size = info.st_size
                    modified = Crawler2.convert_date(info.st_mtime) + ' ' + \
                               Crawler2.convert_time(info.st_mtime)

                    created = Crawler2.convert_date(info.st_ctime) + ' ' + \
                              Crawler2.convert_time(info.st_ctime)

                    accessed = Crawler2.convert_date(info.st_atime) + ' ' + \
                               Crawler2.convert_time(info.st_atime)

                    record = Record(parent=parent_id, directory=directory_flag, name=name,
                                    file_type='',
                                    size=file_size, created=created, modified=modified,
                                    accessed=accessed, read_only=False, hidden=False)

                    database.create_new_entry(record)
                    self.files_processed += 1

                    if entry.is_dir():
                        new_directory = directory + '/' + name
                        self.crawl_directory(new_directory, database.get_current_id() - 1)

                    time.sleep(0)

                    if self.stop_request.isSet():
                        return

            else:
                return

        except:
            print("Unexpected error:", sys.exc_info()[0])
            print(sys.exc_info()[1])

    @staticmethod
    def convert_date(timestamp):

        try:
            d = datetime.utcfromtimestamp(timestamp)
            formatted_date = d.strftime('%d %b %Y')
            return formatted_date
        except:
            print("Unexpected error:", sys.exc_info()[0])
            print(sys.exc_info()[1])

    @staticmethod
    def convert_time(timestamp):

        try:
            d = datetime.utcfromtimestamp(timestamp)
            formatted_time = d.strftime('%H:%M:%S')
            return formatted_time
        except:
            print("Unexpected error:", sys.exc_info()[0])
            print(sys.exc_info()[1])
