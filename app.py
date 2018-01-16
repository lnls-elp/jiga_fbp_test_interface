#!/usr/bin/python3
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.uic import loadUiType

UI_PATH = 'wizard.ui'
Ui_Class, base = loadUiType(UI_PATH)

class TestFbpWindow(QWidget, Ui_Class):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
