# create_new_password.py
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from src.database import *
from src.setuplogger import setup_logger

# TODO добавить теги для пароолей
# тег wifi
# тег site
# тег token итд

class CreateNewPassword(QDialog):
    password_created = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)

        with open("src/assets/styles/dialog_styles.qss", "r") as styles_file:
            style = styles_file.read()
            logger.success(f"Styles for the {__name__} window have been loaded")

        self.setStyleSheet(style)
        styles_file.close()

        self.setWindowTitle("New password")
        self.setFixedSize(400, 400)

        self.new_password_ui()
        # self.save_btn.clicked.connect(self._on_save)
        
    def new_password_ui(self):
        self.new_password_layout = QVBoxLayout()

        self.new_password_input_layout = QFormLayout()
        self.new_password_input_layout.setFormAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.new_password_input_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        self.new_password_input_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)


        message = QLabel(f"Create new password")
        message.setStyleSheet("font-weight: bold;")
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.input_service = QLineEdit()
        # self.input_service.setFixedHeight(30)
        self.input_service.setPlaceholderText("example.com")

        self.input_url = QLineEdit()
        self.input_url.setPlaceholderText("https://github.com/makwells")
        self.input_login = QLineEdit()
        # self.input_login.setFixedHeight(30)
        self.input_login.setPlaceholderText("example@gmail.com")
        self.input_password = QLineEdit()
        # self.input_password.setFixedHeight(30)
        self.input_password.setPlaceholderText("example123456789")

        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept) # Triggers QDialog built-in accept state
        buttons.rejected.connect(self.reject) # Triggers QDialog built-in reject state

        new_password_input_layout_elements = {
            "Service:":self.input_service,
            "URL:":self.input_url,
            "Login:":self.input_login,
            "Password:":self.input_password
        }

        for new_input_name, new_input_elements in new_password_input_layout_elements.items():
            self.new_password_input_layout.addRow(new_input_name, new_input_elements)
        
        self.new_password_layout.addWidget(message)
        self.new_password_layout.addLayout(self.new_password_input_layout)
        self.new_password_layout.addWidget(buttons)

        self.setLayout(self.new_password_layout)

        self.show()

    def _on_save(self):
        service = self.input_service.text().strip()
        login = self.input_login.text().strip()

        if not service or login: 
            return 

        data = {
            "service": service,
            "url": self.input_url.text().strip(),
            "login": login,
            "password": self.input_password.text(),
            # "description": self.input_description.toPlainText(),
        }
        self.password_created.emit(data)
        self.accept()

    def reject(self):
        logger.debug("new password window clicked reject")
        # close_db()
        super().reject()
    
    def accept(self):
        logger.debug("new password window clicked accept")
        self.create_password(self.input_service.text(), self.input_url.text(), self.input_login.text(), self.input_password.text())
        super().accept() 


    def create_password(self, service, url, login, password):
        init_db()
        add_password(service, url, login, password)
        

        
