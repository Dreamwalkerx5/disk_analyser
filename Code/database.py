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

        try:

            c = db.cursor()
            c.execute('''CREATE TABLE DiskTree(id INTEGER PRIMARY KEY, 
                      Parent INTEGER,
                      Directory BOOL, 
                      Name TEXT, 
                      Type TEXT,
                      Size INTEGER,
                      Created,
                      Modified,
                      Accessed,
                      Read_only BOOL,
                      Hidden BOOL)''')
            db.commit()

            print("New database created.")

        except:

            print("Unexpected error:", sys.exc_info()[0])
            print(sys.exc_info()[1])

    def create_new_entry(self, parent=None, directory=False, name='', file_type='', size=0,
                         created='', modified='', accessed='', read_only=False, hidden=False):

        pass

    def get_entry(self, entry_id=0):

        text = ''

        return text

class Record:

    def __init__(self, entry_id=0, parent=None, directory=False, name='', file_type='', size=0,
                 created='', modified='', accessed='', read_only=False, hidden=False):

        self.entry_id = entry_id
        self.parent = parent
        self.directory = directory
        self.name = name
        self.file_type = file_type
        self.size = size
        self.created = created
        self.accessed = accessed
        self.modified = modified
        self.read_only = read_only
        self.hidden = hidden

    def entry_id(self):

        return self.entry_id()

    def parent(self):

        return self.parent()

    def directory(self):

        return self.directory()



