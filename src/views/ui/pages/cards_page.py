from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

class Cards_page(QObject):
    def __init__(self):
        super().__init__()
        self.cards_page()

    def cards_page(self):
        self.cards_widget = QWidget()
        self.cards_widget.setObjectName("RightWorkspace")
        self.cards_layout = QVBoxLayout(self.cards_widget)

        title = QLabel("Cards")
        title.setStyleSheet("font-size: 24pt;")

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)


        self.cards_layout.addWidget(title)
        self.cards_layout.addWidget(scroll_area)
        