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

        self.setWindowTitle("Settings")
        self.resize(800, 600)

        self.settings_ui()
    
    def settings_ui(self):

        self.show()
