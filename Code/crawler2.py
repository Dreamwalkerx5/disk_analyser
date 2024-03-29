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
    # Connect signals to correct GUI methods
    finished_signal = pyqtSignal('PyQt_PyObject')
    info_signal = pyqtSignal('PyQt_PyObject')
    progress_signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent=None, gui=None, root=None, parent_id=0, kill_signal=None):
        QThread.__init__(self)

        self.parent = parent
        self.gui = gui
        self.files_processed = 0
        self.total_files = 0
        self.root = root
        self.parent_id = parent_id
        self.stop_request = False
        self.recursion = 0
        self.max_recursion = 0
        self.kill_signal = kill_signal
        self.kill_signal.connect(self.kill)

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

                    name = entry.name[0:len(entry.name) - len(entry.suffix)]
                    suffix = entry.suffix
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
                                    file_type=suffix,
                                    size=file_size, created=created, modified=modified,
                                    accessed=accessed, read_only=False, hidden=False)

                    database.create_new_entry(record)
                    self.files_processed += 1
                    self.progress_signal.emit(int((self.files_processed / self.total_files) * 100))

                    if entry.is_dir():
                        new_directory = directory + '/' + entry.name
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

        self.info_signal.emit(f'Crawling disk. Done {self.files_processed} of {self.total_files}  '
                              f'Max recursion: {self.max_recursion}  '
                              f'Current recursion: {self.recursion}')

    def kill(self):
        print('Crawler thread dying...')
        self.stop_request = True

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
