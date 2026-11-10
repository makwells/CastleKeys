#wifi_page.py
from PySide6.QtCore import QObject
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

class WiFi_page(QObject):
    def __init__(self):
        super().__init__()
        self.wifi_page()

    def wifi_page(self):
        self.wifi_widget = QWidget()
        self.wifi_widget.setObjectName("RightWorkspace")
        self.wifi_layout = QVBoxLayout(self.wifi_widget)

        title = QLabel("Wi-Fi")
        title.setStyleSheet("font-size: 24pt;")

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)


        self.wifi_layout.addWidget(title)
        self.wifi_layout.addWidget(scroll_area)
        