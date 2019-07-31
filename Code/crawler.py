import sys
import threading
from datetime import datetime
from pathlib import Path

from PyQt5 import QtGui

from Code.database import Record


class Crawler:

    @staticmethod
    def crawl_disk(gui, ui, database, root, parent):

        ui.info_label.setText('Crawling disk...')

        # Start crawler thread
        crawler_thread = threading.Thread(target=Crawler.do_crawl(gui, ui, database, root, parent))
        crawler_thread.start()
        return crawler_thread

    @staticmethod
    def do_crawl(gui, ui, database, root, parent):

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
                    Crawler.crawl_disk(gui, ui, database, new_root, database.id_count - 1)

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
