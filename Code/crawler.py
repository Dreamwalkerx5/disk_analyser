import sys
from pathlib import Path


class Crawler:

    @staticmethod
    def crawl_disk(ui, database, root):

        print('Crawling disk...')

        try:

            entries = Path(root)
            for entry in entries.iterdir():
                print(entry.name)

        except:

            print("Unexpected error:", sys.exc_info()[0])
            print(sys.exc_info()[1])
