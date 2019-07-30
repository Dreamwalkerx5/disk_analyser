import sqlite3
import sys


class Database:

    def __init__(self, gui):
        self.db = self.open_database(gui)
        self.gui = gui

    def clear_database(self):

        # Delete old database
        try:
            c = self.db.cursor()
            c.execute('DROP TABLE IF EXISTS DiskTree ')
            self.db.commit()

            # Create new database
            Database.create_new_database(self.db)
            self.gui.info_label.setText('Database has been cleared.')
            print('Database cleared')

        except:

            print("Unexpected error:", sys.exc_info()[0])
            print(sys.exc_info()[1])

    @staticmethod
    def open_database(gui):

        try:
            # open a connection to sqlite3
            db = sqlite3.connect('Disk.db')

            # check if database exists
            c = db.cursor()
            c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='DiskTree' ''')
            if not c.fetchone()[0]:

                Database.create_new_database(db)
                gui.info_label.setText('New database created and a connection made.')
                print('New database created')

            else:

                gui.info_label.setText('Database found and a connection made.')
                print('Database found and opened')

            db.commit()

            return db

        except:

            print("Unexpected error:", sys.exc_info()[0])
            print(sys.exc_info()[1])

    def close_database(self):

        self.db.close()
        print('Database closed')

    @staticmethod
    def create_new_database(db):

        c = db.cursor()
        c.execute('''CREATE TABLE DiskTree(id INTEGER PRIMARY KEY, created TIMESTAMP, category TEXT, entry TEXT)''')
        db.commit()

        print("New database created.")

