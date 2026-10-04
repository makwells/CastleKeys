#all_passwords.py
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

class AllPasswordsPage:
    def __init__(self):
        self.all_passwords_page_ui()

    def all_passwords_page_ui(self):
        self.all_passwords_widget = QWidget()
        self.all_passwords_widget.setObjectName("RightWorkspace")

        self.add_section()

        self.all_passwords_layout = QVBoxLayout(self.all_passwords_widget)
        self.all_passwords_layout.addWidget(self.top_section_widget)
        self.all_passwords_layout.addWidget(self.bottom_section_widget)


    def add_section(self):
        self.top_section_widget = QWidget()
        self.top_section_layout = QHBoxLayout(self.top_section_widget)
        self.bottom_section_widget = QWidget()
        self.bottom_section_layout = QHBoxLayout(self.bottom_section_widget)

        #top section 
        self.service_icon = ...
        self.service_name = QLabel("Example")
        self.favorite_btn = QPushButton("<3")

        self.top_section_layout.addWidget(self.service_name)
        self.top_section_layout.addStretch()
        self.top_section_layout.addWidget(self.favorite_btn)

        #bottom section 
        self.service_url = QLabel("https://example.com/")
        self.creation_date = QLabel("01.12.26")

        self.bottom_section_layout.addWidget(self.service_url)
        self.bottom_section_layout.addStretch()
        self.bottom_section_layout.addWidget(self.creation_date)

        # self.section_layout.addLayout(self.top_section_layout)
        # self.section_layout.addLayout(self.bottom_section_layout)
        