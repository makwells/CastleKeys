#tokens_page.py 

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from src.setuplogger import *

class Tokens_page(QObject):
    def __init__(self):
        super().__init__()

        self.tokens_page()

    def tokens_page(self):
        self.tokens_widget = QWidget()
        self.tokens_layout = QVBoxLayout(self.tokens_widget)

        title = QLabel("Tokens")
        title.setStyleSheet("font-size: 24pt;")

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        self.tokens_layout.addWidget(title)
        self.tokens_layout.addWidget(scroll_area)
