import sys, time
import threading
from datetime import datetime
from pathlib import Path

from PyQt5 import QtGui

from Code.database import Record
from Code.database import Database


class Crawler:

    def __init__(self):

        self.crawler_thread = None

    def crawl_disk(self, ui=None, database=None, root=None, parent=None):

        # ui.info_label.setText('Crawling disk...')

        # Start crawler thread
        self.crawler_thread = threading.Thread(target=self.do_crawl,
                                               args=(ui, database, root, parent,), daemon=True)
        self.crawler_thread.start()

    def do_crawl(self, *args):

        ui = args[0]
        database = args[1]
        root = args[2]
        parent = args[3]

        database = Database(ui)

        try:

            entries = Path(root)
            for entry in entries.iterdir():

                name = entry.name
                info = entry.stat()
                if entry.is_dir():

                    directory = True

                else:

                    directory = False

                file_size = info.st_size
                modified = Crawler.convert_date(info.st_mtime) + ' ' + \
                           Crawler.convert_time(info.st_mtime)

                created = Crawler.convert_date(info.st_ctime) + ' ' + \
                          Crawler.convert_time(info.st_ctime)

                accessed = Crawler.convert_date(info.st_atime) + ' ' + \
                           Crawler.convert_time(info.st_atime)

                record = Record(parent=parent, directory=directory, name=name, file_type='',
                                size=file_size, created=created, modified=modified,
                                accessed=accessed, read_only=False, hidden=False)

                database.create_new_entry(record)

                if entry.is_dir():
                    new_root = root + '/' + name
                    self.crawl_disk(ui, database, new_root, database.id_count - 1)

                time.sleep(0)

        except:

            print("Unexpected error:", sys.exc_info()[0])
            print(sys.exc_info()[1])

    @staticmethod
    def convert_date(timestamp):
        d = datetime.utcfromtimestamp(timestamp)
        formatted_date = d.strftime('%d %b %Y')
        return formatted_date

    @staticmethod
    def convert_time(timestamp):
        d = datetime.utcfromtimestamp(timestamp)
        formatted_time = d.strftime('%H:%M:%S')
        return formatted_time
