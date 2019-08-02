#  Copyright (c) 2019. Steven Taylor All rights reserved

import time
from datetime import datetime

from PyQt5.QtCore import QThread, pyqtSignal


class Clock(QThread):
    time_signal = pyqtSignal('PyQt_PyObject')

    def __init__(self):
        QThread.__init__(self)

        self.stop_request = False

    def run(self):
        while not self.stop_request:
            current_time = str(datetime.now())
            self.time_signal.emit(current_time[11:19])
            time.sleep(1)
