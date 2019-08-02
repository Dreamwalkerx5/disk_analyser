#  Copyright (c) 2019. Steven Taylor All rights reserved
import sys
from PyQt5.QtCore import QThread, pyqtSignal
import time
from datetime import datetime
from pathlib import Path

from Code.database import Record
from Code.database import Database


class Crawler2(QThread):
    files_processed: int
    finished_signal = pyqtSignal('PyQt_PyObject')
    info_signal = pyqtSignal('PyQt_PyObject')
    progress_signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent=None, gui=None, root=None, parent_id=0):
        QThread.__init__(self)

        self.parent = parent
        self.gui = gui
        self.files_processed = 0
        self.total_files = 0
        self.root = root
        self.parent_id = parent_id
        self.stop_request = False
        self.crawler_monitor = None
        self.recursion = 0
        self.max_recursion = 0

    def run(self):
        try:
            # Calculate total files
            self.info_signal.emit('Calculating number of files...')
            self.total_files = self.parent.file_counter()

            self.info_signal.emit('Crawling disk...')
            self.crawl_directory(self.root, self.parent_id)
            self.info_signal.emit('Finished disk crawl.')

            # Update view
            self.finished_signal.emit(0)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            print(sys.exc_info()[1])

    def crawl_directory(self, directory, parent_id):
        self.update_info()
        self.recursion += 1
        if self.recursion > self.max_recursion:
            self.max_recursion = self.recursion

        try:
            # Check if thread has been told to stop
            if not self.stop_request:
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

                    if self.stop_request:
                        return

                self.recursion -= 1
                self.update_info()

            else:
                return

        except:
            print("Unexpected error:", sys.exc_info()[0])
            print(sys.exc_info()[1])

    def update_info(self):

        self.info_signal.emit('Crawling disk... Max recursion: ' + str(self.max_recursion) +
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
