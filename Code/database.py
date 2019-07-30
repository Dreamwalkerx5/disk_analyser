import sqlite3


class Database:

    def __init__(self, gui):
        self.db = self.open_database()
        self.gui = gui

    def open_database(self, gui):

        # open a connection to sqlite3
        db = sqlite3.connect('Disk.db')

        # check if database exists
        c = db.cursor()
        c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='DiskTree' ''')
        if not c.fetchone()[0]:
            Database.create_new_database(gui, db)
        else:
            gui.info_label.setText('Database found and a connection made.')

        db.commit()

        return db

    def create_new_database(self, gui, db):
        c = db.cursor()
        c.execute('''CREATE TABLE journal(id INTEGER PRIMARY KEY, created TIMESTAMP, category TEXT, entry TEXT)''')
        c.execute('''CREATE TABLE info(id INTEGER PRIMARY KEY, created TIMESTAMP, keywords TEXT, info TEXT)''')
        db.commit()

        print("New database created.")
        gui.info_label.setText('New database created and a connection made')
