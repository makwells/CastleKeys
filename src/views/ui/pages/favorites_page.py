#favorites_page.py
from PySide6.QtCore import QObject
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

class Favorites_page(QObject):
    def __init__(self):
        super().__init__()
        self.favorites_page()

    def favorites_page(self):
        self.favorites_widget = QWidget()
        self.favorites_widget.setObjectName("RightWorkspace")
        self.favorites_layout = QVBoxLayout(self.favorites_widget)

        title = QLabel("Favorites")
        title.setStyleSheet("font-size: 24pt;")

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)


        self.favorites_layout.addWidget(title)
        self.favorites_layout.addWidget(scroll_area)
        