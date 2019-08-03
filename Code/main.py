#  Copyright (c) 2019. Steven Taylor All rights reserved
import os
from datetime import datetime
import sys
import threading
import time

from PyQt5.QtCore import pyqtSignal

from Code.gui import Ui_mainWindow
from Code.database import Database, Record
from Code.crawler2 import Crawler2
from Code.clock import Clock
from Code.utils import pad_string

from PyQt5 import QtWidgets, QtGui, QtCore


class Gui(QtWidgets.QMainWindow):
    clock_kill_signal = pyqtSignal('PyQt_PyObject')
    crawler_kill_signal = pyqtSignal('PyQt_PyObject')

    def __init__(self):
        super(Gui, self).__init__()

        # Create main window gui
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)

        # Setup listeners
        self.ui.clear_button.clicked.connect(self.clear_database)
        self.ui.quit_button.clicked.connect(self.quit)
        self.ui.crawl_button.clicked.connect(self.crawler)
        self.ui.listView.clicked.connect(self.item_selected)
        self.ui.count_button.clicked.connect(self.file_counter)

        # Open sql database
        self.database = Database(self.ui)

        # create model for the listview
        self.model = QtGui.QStandardItemModel(self.ui.listView)
        self.ui.listView.setModel(self.model)

        # Set up some variables
        self.current_root = "C:/Users/steve/PycharmProjects/disk_analyser"
        # self.current_root = "C:/Users/steve"
        self.current_parent = 0
        self.previous_parent = 0
        self.display_index = []
        self.crawler_thread = None

        # Start clock thread
        self.clock = Clock(self.clock_kill_signal)
        self.clock.time_signal.connect(self.update_time_label)

        self.clock.start()

        # Create initial display
        self.ui.info_label.setText('Welcome to Disk Analyser v1.0')
        self.create_view()

    def update_time_label(self, new_time):
        self.ui.time_label.setText(new_time)

    def clock_thread(self):
        while True:
            current_time = str(datetime.now())
            self.ui.time_label.setText(current_time[11:19])
            time.sleep(1)

    def file_counter(self):

        try:

            cpt = sum([len(files) for root, dirs, files in os.walk(self.current_root)])
            self.ui.info_label.setText('Total files: ' + str(cpt))
            return cpt

        except:

            print("Unexpected error:", sys.exc_info()[0])
            print(sys.exc_info()[1])

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def item_selected(self, index):

        # Get id of selected item
        selection = self.display_index[index.row()]
        if index.row() == 0:

            record = self.database.get_entry(self.current_parent)
            self.current_parent = record.parent

        else:

            record = self.database.get_entry(selection)

            if record.directory:

                self.current_parent = selection
                print(record.directory)

        self.create_view()

    def close_database(self):

        self.database.close_database()

    def clear_database(self):

        self.database.clear_database()
        self.create_view()

    def crawler(self):

        self.clear_database()
        # Create crawler thread
        self.crawler_thread = Crawler2(parent=self, gui=self.ui,
                                       root=self.current_root, parent_id=0,
                                       kill_signal=self.crawler_kill_signal)
        # Connect finished signal to our method
        self.crawler_thread.finished_signal.connect(self.crawler_finished)
        self.crawler_thread.info_signal.connect(self.update_info)
        self.crawler_thread.progress_signal.connect(self.update_progress_bar)

        self.crawler_thread.start()

    def crawler_finished(self, result):
        self.create_view()

    def create_view(self):

        self.model.clear()
        self.display_index.clear()
        # Get new instance of database in case we are running in a different thread
        temp_database = Database(self.ui)

        records = temp_database.get_all(parent=self.current_parent)
        # Set parent as first item
        self.display_index.append(0)
        self.model.appendRow(QtGui.QStandardItem('...'))

        for temp_record in records:

            temp_string = ''
            # temp_string += f'{temp_record.parent}  '
            if temp_record.directory:
                temp_string += '*'
            else:
                temp_string += ' '

            temp_string += pad_string(text=temp_record.name, length=50, pad_char='.', back=True) + ' '

            if temp_record.size < 1024:
                temp_string += pad_string(text=f'{temp_record.size:.2f}B',
                                          length=10, pad_char=' ', back=False)
            elif temp_record.size < 104858:
                temp_string += pad_string(text=f'{(temp_record.size / 1024):.2f}K',
                                          length=10, pad_char=' ', back=False)
            elif temp_record.size < 107374183:
                temp_string += pad_string(text=f'{(temp_record.size / 1048576):.2f}M',
                                          length=10, pad_char=' ', back=False)
            else:
                temp_string += pad_string(text=f'{(temp_record.size / 1073741824):.2f}G',
                                          length=10, pad_char=' ', back=False)

            self.display_index.append(temp_record.entry_id)
            item = QtGui.QStandardItem(temp_string)
            self.model.appendRow(item)

    def quit(self):
        if self.crawler_thread is not None:
            if self.crawler_thread.isRunning():
                self.crawler_kill_signal.emit(0)
                self.crawler_thread.wait()

        self.clock_kill_signal.emit(0)
        self.clock.wait()

        self.close_database()
        app.quit()

    def update_progress_bar(self, progress):
        self.ui.progressBar.setValue(progress)

    def update_info(self, text):
        self.ui.info_label.setText(text)


record = Record(entry_id=0, parent=None, directory=True, name='root', file_type='', size=0,
                created='30/06/2019', modified='30/06/2019', accessed='30/06/2019',
                read_only=False, hidden=False)


app = QtWidgets.QApplication([])

# Create my GUI
gui = Gui()
gui.show()

# Run main loop
app.exec()

print('Quit...')
sys.exit()
