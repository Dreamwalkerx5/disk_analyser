# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\steve\PycharmProjects\disk_analyser\code\gui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.info_label = QtWidgets.QLabel(self.centralwidget)
        self.info_label.setGeometry(QtCore.QRect(40, 500, 711, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.info_label.setFont(font)
        self.info_label.setStyleSheet("background-color:white")
        self.info_label.setFrameShape(QtWidgets.QFrame.Box)
        self.info_label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.info_label.setAlignment(QtCore.Qt.AlignCenter)
        self.info_label.setObjectName("info_label")
        self.time_label = QtWidgets.QLabel(self.centralwidget)
        self.time_label.setGeometry(QtCore.QRect(630, 70, 121, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.time_label.setFont(font)
        self.time_label.setStatusTip("")
        self.time_label.setFrameShape(QtWidgets.QFrame.Box)
        self.time_label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.time_label.setObjectName("time_label")
        self.quit_button = QtWidgets.QPushButton(self.centralwidget)
        self.quit_button.setGeometry(QtCore.QRect(650, 370, 101, 41))
        self.quit_button.setObjectName("quit_button")
        self.clear_button = QtWidgets.QPushButton(self.centralwidget)
        self.clear_button.setGeometry(QtCore.QRect(650, 330, 101, 28))
        self.clear_button.setObjectName("clear_button")
        self.crawl_button = QtWidgets.QPushButton(self.centralwidget)
        self.crawl_button.setGeometry(QtCore.QRect(650, 290, 101, 28))
        self.crawl_button.setObjectName("crawl_button")
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "Disk Analyser"))
        self.info_label.setText(_translate("mainWindow", "TextLabel"))
        self.time_label.setToolTip(_translate("mainWindow", "Current time"))
        self.time_label.setText(_translate("mainWindow", "12:00:00"))
        self.quit_button.setText(_translate("mainWindow", "Quit"))
        self.clear_button.setText(_translate("mainWindow", "Clear Database"))
        self.crawl_button.setText(_translate("mainWindow", "Crawl Disk"))

