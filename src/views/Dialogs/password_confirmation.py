#password_confirmation.py
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from src.setuplogger import *

from src.config_manager import ConfigManager

class Password_Confirmation(QDialog):

    password = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        config_manager = ConfigManager()
        dialog_style = config_manager.get_dialog_style()
        self.setStyleSheet(dialog_style)
        self.password_confirmation_window()

    def password_confirmation_window(self):
        logger.success("The confirmation password box has been loaded")
        self.setWindowTitle("Confirmation") #title 
        self.setFixedSize(400, 200) # window size
        self.setWindowFlags(Qt.FramelessWindowHint) #hide window borders

        layout = QVBoxLayout()

        #message
        message = QLabel(f"Confirm password")
        message.setStyleSheet("font-weight: bold;") #message font bold paramenter
        message.setAlignment(Qt.AlignmentFlag.AlignCenter) #message aligment

        self._password_field = QLineEdit()
        self._password_field.setPlaceholderText("Password: ")
        self._password_field.textChanged.connect(self.confirmation)
        ok_button = QPushButton("Ok")
        ok_button.clicked.connect(self.accept)

        layout.addWidget(message)
        layout.addWidget(self._password_field)
        layout.addWidget(ok_button)

        self.setLayout(layout)

    def confirmation(self):
        self.data = {"password": self._password_field.text().strip()}

    def accept(self):
        super().accept()
        self.password.emit(self.data)
