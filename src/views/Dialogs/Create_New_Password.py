# Create_New_Password.py
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from src.database import *
from src.setuplogger import setup_logger

# TODO добавить теги для пароолей
# тег wifi
# тег site
# тег token итд

#c7c7c7

class CreateNewPassword(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        setup_logger()

        with open("src/assets/styles/dialog_styles.qss", "r") as styles_file:
            style = styles_file.read()
            logger.success("Styles for the dialog window have been loaded")

        logger.info("The style file for the dialog box is open")
        self.setStyleSheet(style)
        styles_file.close()
        logger.info("The style file for the dialog box is closed")
        

        self.setWindowTitle("New password")
        self.setFixedSize(400, 400)

        self.new_password_ui()
        
    def new_password_ui(self):
        self.new_password_layout = QVBoxLayout()
        message = QLabel(f"Create new password")
        message.setStyleSheet("font-weight: bold;")
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.label_service = QLabel("Service:")
        self.input_service = QLineEdit()
        self.input_service.setFixedHeight(30)
        self.input_service.setPlaceholderText("example.com")
        self.label_login = QLabel("Login:")
        self.input_login = QLineEdit()
        self.input_login.setFixedHeight(30)
        self.input_login.setPlaceholderText("example@gmail.com")
        self.label_password = QLabel("Password:")
        self.input_password = QLineEdit()
        self.input_password.setFixedHeight(30)
        self.input_password.setPlaceholderText("example123456789")

        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept) # Triggers QDialog built-in accept state
        buttons.rejected.connect(self.reject) # Triggers QDialog built-in reject state
        
        self.new_password_layout.addWidget(message)
        self.new_password_layout.addWidget(self.label_service)
        self.new_password_layout.addWidget(self.input_service)
        self.new_password_layout.addWidget(self.label_login)
        self.new_password_layout.addWidget(self.input_login)
        self.new_password_layout.addWidget(self.label_password)
        self.new_password_layout.addWidget(self.input_password)
        self.new_password_layout.addWidget(buttons)

        self.setLayout(self.new_password_layout)

        self.show()

    def reject(self):
        logger.debug("new password window clicked reject")
        close_db()
        super().reject()
    
    def accept(self):
        logger.debug("new password window clicked accept")
        self.create_password(self.input_service.text(), self.input_login.text(), self.input_password.text())
        super().accept() 


    def create_password(self, service, login, password):
        init_db()
        add_password(service, login, password)
        close_db()
        

        
