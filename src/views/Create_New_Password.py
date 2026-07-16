# Create_New_Password.py
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from ..views.main_window import MainWindow
from src.database import *


# TODO добавить теги для пароолей
# тег wifi
# тег site
# тег token итд

#c7c7c7

class CreateNewPassword(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("New password")
        self.setFixedSize(400, 300)

        self.new_password_ui()
        
        init_db()

    def new_password_ui(self):
        layout = QVBoxLayout()
        message = QLabel(f"Create new password")
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.label_service = QLabel("Service:")
        self.input_service = QLineEdit()
        self.input_service.setPlaceholderText("example.com")
        self.label_login = QLabel("Login:")
        self.input_login = QLineEdit()
        self.input_login.setPlaceholderText("example@gmail.com")
        self.label_password = QLabel("Password:")
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("example123456789")

        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept) # Triggers QDialog built-in accept state
        buttons.rejected.connect(self.reject) # Triggers QDialog built-in reject state
        
        layout.addWidget(message)
        layout.addWidget(self.label_service)
        layout.addWidget(self.input_service)
        layout.addWidget(self.label_login)
        layout.addWidget(self.input_login)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(buttons)
    
        self.setLayout(layout)

        self.show()
    
    def accept(self):
        self.create_password(self.input_service.text(), self.input_login.text(), self.input_password.text())
        super().accept() 


    def create_password(self, service, login, password):
        add_password(service, login, password)




        
