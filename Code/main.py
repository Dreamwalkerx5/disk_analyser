# Disk Analyser v1.0
# Copyright (c) 2019 Steven Taylor All rights reserved
import datetime
import sys
import time

from Code.gui import Ui_mainWindow
from Code.database import Database

from PyQt5 import QtWidgets, QtGui, QtCore


class Gui(QtWidgets.QMainWindow):

    def __init__(self):
        super(Gui, self).__init__()

        # Create main window gui
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)

        # Setup listeners
        self.ui.clear_button.clicked.connect(self.clear_database)
        self.ui.quit_button.clicked.connect(self.quit)

        # Open sql database
        self.database = Database(self.ui)

    def clock_thread(self):
        while True:
            current_time = str(datetime.now())
            self.ui.time_label.setText(current_time[11:19])
            time.sleep(1)

    def close_database(self):

        self.database.close_database()

    def clear_database(self):

        self.database.clear_database()

    def quit(self):

        self.close_database()
        app.quit()


app = QtWidgets.QApplication([])

# Create my GUI
gui = Gui()
gui.show()

# Run main loop
app.exec()

print('Quit...')
sys.exit()
