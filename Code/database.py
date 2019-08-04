#  Copyright (c) 2019. Steven Taylor All rights reserved

import sqlite3
import sys
import threading


class Database:

    id_count = 1
    lock = threading.Lock()

    def __init__(self, gui):
        self.db = self.open_database(gui)
        self.gui = gui
        # self.id_count = 0

    def clear_database(self):

        # Delete old database
        try:
            c = self.db.cursor()
            c.execute('DROP TABLE IF EXISTS DiskTree ')
            self.db.commit()

            # Create new database
            Database.id_count = 1
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

                pass
                # gui.info_label.setText('Database found and a connection made.')
                # print('Database found and opened')

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
            c.execute('''CREATE TABLE DiskTree(Id INTEGER PRIMARY KEY, 
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

    def create_new_entry(self, record=None):

        # Acquire thread lock
        Database.lock.acquire()

        c = self.db.cursor()

        entry = (self.id_count, record.parent, record.directory, record.name, record.file_type
                 , record.size, record.created, record.modified, record.accessed
                 , record.read_only, record.hidden, )

        c.execute('''INSERT INTO DiskTree(Id, Parent, Directory, Name, Type, Size, Created, Modified, 
                  accessed, Read_only, Hidden) VALUES(?,?,?,?,?,?,?,?,?,?,?)''', entry)

        self.db.commit()

        Database.id_count += 1

        # Release thread lock
        Database.lock.release()

    def get_entry(self, entry_id=1):

        try:

            c = self.db.cursor()

            c.execute('SELECT * FROM DiskTree WHERE Id=?', (entry_id,))

            row = c.fetchone()

            record = Record(entry_id=row[0], parent=row[1], directory=row[2], name=row[3], file_type=row[4],
                            size=row[5], created=row[6], modified=row[7], accessed=row[8],
                            read_only=row[9], hidden=row[10])

            return record

        except:

            print("Unexpected error:", sys.exc_info()[0])
            print(sys.exc_info()[1])

    def get_all(self, parent=0):

        try:

            records = []
            c = self.db.cursor()

            c.execute('SELECT * FROM DiskTree WHERE Parent= ? ORDER BY Id', (parent,))

            for row in c:

                record = Record(entry_id=row[0], parent=row[1], directory=row[2], name=row[3], file_type=row[4],
                                size=row[5],
                                created=row[6], modified=row[7], accessed=row[8],
                                read_only=row[9], hidden=row[10])

                records.append(record)

            return records

        except:

            print("Unexpected error:", sys.exc_info()[0])
            print(sys.exc_info()[1])

    @staticmethod
    def get_current_id():
        Database.lock.acquire()
        id = Database.id_count
        Database.lock.release()
        return id


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

        return self.entry_id

    def parent(self):
        return self.parent

    def directory(self):
        return self.directory

    def name(self):
        return self.name

    def file_type(self):
        return self.file_type

    def size(self):
        return self.size

    def created(self):
        return self.created

    def accessed(self):
        return self.accessed

    def modified(self):
        return self.modified

    def read_only(self):
        return self.read_only

    def hidden(self):
        return self.hidden
