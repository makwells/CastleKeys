#notificatons_window.py 
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *


class Notifications(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(150, 150)
        # self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setWindowFlags(
            Qt.FramelessWindowHint | 
            Qt.WindowStaysOnTopHint | 
            Qt.Tool
        )

        self.layout_not = QVBoxLayout(self)
        self.layout_not.addWidget(QLabel("Я привязано к главному окну!"))