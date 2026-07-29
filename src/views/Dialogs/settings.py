from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from src.database import *

class Settings(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        

        with open("src/assets/styles/dialog_styles.qss", "r") as styles_file:
            style = styles_file.read()

        self.setStyleSheet(style)
        self.settings_ui()
    
    def settings_ui(self):
        self.setWindowTitle("Settings")
        self.resize(800, 600)

        self.main_block = QHBoxLayout()

        self.storage_block = QVBoxLayout()

        self.path_to_passwords = QLineEdit()
        self.path_to_passwords.setPlaceholderText(".Passwords")
        self.storage_block.addWidget(self.path_to_passwords)

        self.main_block.addLayout(self.storage_block)
        self.setLayout(self.main_block)
        self.show()
