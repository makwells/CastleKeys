#contacts_page.py 

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from src.setuplogger import *

class Contacts_page(QObject):
    def __init__(self):
        super().__init__()

        self.contacts_page()

    def contacts_page(self):
        self.contacts_widget = QWidget()
        self.contacts_layout = QVBoxLayout(self.contacts_widget)

        title = QLabel("Contacts")
        title.setStyleSheet("font-size: 24pt;")

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        self.contacts_layout.addWidget(title)
        self.contacts_layout.addWidget(scroll_area)
