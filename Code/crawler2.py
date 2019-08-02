#  Copyright (c) 2019. Steven Taylor All rights reserved
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

from Code.database import Record
from Code.database import Database


class Crawler2(threading.Thread):
    files_processed: int

    def __init__(self, parent=None, gui=None, root=None, parent_id=0):
        super(Crawler2, self).__init__()

        self.parent = parent
        self.gui = gui
        self.files_processed = 0
        self.total_files = 0
        self.root = root
        self.parent_id = parent_id
        self.stop_request = threading.Event()
        self.crawler_monitor = None
        self.recursion = 0
        self.max_recursion = 0

    def run(self):
        try:
            # Calculate total files
            self.gui.info_label.setText('Calculating number of files...')
            self.total_files = self.parent.file_counter()

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
        self.update_info()
        self.recursion += 1
        if self.recursion > self.max_recursion:
            self.max_recursion = self.recursion

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
                    self.parent.update_progress_bar(int((self.files_processed / self.total_files) * 100))

                    if entry.is_dir():
                        new_directory = directory + '/' + name
                        self.crawl_directory(new_directory, database.get_current_id() - 1)

                    time.sleep(0)

                    if self.stop_request.isSet():
                        return

                self.recursion -= 1
                self.update_info()

            else:
                return

        except:
            print("Unexpected error:", sys.exc_info()[0])
            print(sys.exc_info()[1])

    def update_info(self):

        self.gui.info_label.setText('Crawling disk... Current thread: ' +
                                    str(threading.get_ident()) +
                                    ' Max recursion: ' + str(self.max_recursion) +
                                    ' Current recursion: ' + str(self.recursion))

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
