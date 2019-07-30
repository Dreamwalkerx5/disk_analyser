# Disk Analyser v1.0
# Copyright (c) 2019 Steven Taylor All rights reserved
import datetime
import sys
import time

from gui import Ui_mainWindow

from PyQt5 import QtWidgets, QtGui, QtCore


class Gui(QtWidgets.QMainWindow):

    def __init__(self):
        super(Gui, self).__init__()

        self.ui =
        self.ui.setupUi(self)

    def clock_thread(self):
        while True:
            current_time = str(datetime.now())
            self.ui.time_label.setText(current_time[11:19])
            time.sleep(1)


app = QtWidgets.QApplication([])

# Create my GUI
gui = Gui()
gui.show()

# Run main loop
app.exec()

print('Quit')
sys.exit()
