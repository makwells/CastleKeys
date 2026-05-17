# settings.py

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import *

import sys

class Settings_window(QWidget):
    def __init__(self):
        super().__init__()

        self.settings_UI()

    def settings_UI(self):
        self.setWindowTitle("Settings")
        self.setFixedSize(500, 400)




