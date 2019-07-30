import sqlite3
import sys


class Database:

    def __init__(self, gui):
        self.db = self.open_database(gui)
        self.gui = gui
        self.id_count = 0

    def clear_database(self):

        # Delete old database
        try:
            c = self.db.cursor()
            c.execute('DROP TABLE IF EXISTS DiskTree ')
            self.db.commit()

            # Create new database
            self.id_count = 0
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

        c = self.db.cursor()

        entry = (self.id_count, record.parent, record.directory, record.name, record.file_type
                 , record.size, record.created, record.modified, record.accessed
                 , record.read_only, record.hidden, )

        c.execute('''INSERT INTO DiskTree(Id, Parent, Directory, Name, Type, Size, Created, Modified, 
                  accessed, Read_only, Hidden) VALUES(?,?,?,?,?,?,?,?,?,?,?)''', entry)

        self.db.commit()

        self.id_count += 1

    def get_entry(self, entry_id=1):

        try:

            c = self.db.cursor()

            c.execute('SELECT * FROM DiskTree WHERE Id=?', (entry_id,))

            result = c.fetchone()
            print(result[3])
            record = Record(entry_id=0, parent=None, directory=True, name=result[3], file_type='', size=0,
                            created='30/06/2019', modified='30/06/2019', accessed='30/06/2019',
                            read_only=False, hidden=False)

            return record

        except:

            print("Unexpected error:", sys.exc_info()[0])
            print(sys.exc_info()[1])

    def get_all(self, parent=6):

        try:

            records = []
            c = self.db.cursor()

            c.execute('SELECT * FROM DiskTree WHERE Parent= ? ORDER BY Id', (parent,))

            for row in c:

                record = Record(entry_id=row[0], parent=row[1], directory=True, name=row[3], file_type='', size=0,
                                created=row[6], modified='30/06/2019', accessed='30/06/2019',
                                read_only=False, hidden=False)

                records.append(record)

            return records

        except:

            print("Unexpected error:", sys.exc_info()[0])
            print(sys.exc_info()[1])


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
