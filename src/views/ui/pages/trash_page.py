#trash_page.py
from PySide6.QtCore import QObject
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

class Trash_page(QObject):
    def __init__(self):
        super().__init__()
        self.trash_page()

    def trash_page(self):
        self.trash_widget = QWidget()
        self.trash_layout = QVBoxLayout(self.trash_widget)

        title = QLabel("Trash")
        title.setStyleSheet("font-size: 24pt;")

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)


        self.trash_layout.addWidget(title)
        self.trash_layout.addWidget(scroll_area)
        