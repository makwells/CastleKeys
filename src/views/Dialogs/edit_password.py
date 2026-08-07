#edit_passwords.py
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from src.database import *
from src.setuplogger import setup_logger

class Edit_Password(QDialog):

    data_edit_password = pyqtSignal(object)
    finished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        with open("src/assets/styles/dialog_styles.qss", "r") as styles_file:
            style = styles_file.read()
            logger.success(f"Styles for the {__name__} window have been loaded")

        self.setStyleSheet(style)
        styles_file.close()

        self.setWindowTitle("Edit password")
        self.setFixedSize(400, 400)

        self.edit_password_ui()
    
    def edit_password_ui(self):
        self.edit_password_layout = QVBoxLayout()

        self.edit_input_layout = QFormLayout() 
        self.edit_input_layout.setFormAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.edit_input_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        self.edit_input_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)


        message = QLabel(f"Edit password")
        message.setStyleSheet("font-weight: bold;")
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        
        self.edit_input_service = QLineEdit()
        self.edit_input_url = QLineEdit()
        self.edit_input_login = QLineEdit()
        self.edit_input_password = QLineEdit()
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept) # Triggers QDialog built-in accept state
        buttons.rejected.connect(self.reject) # Triggers QDialog built-in reject state


        edit_input_layout_elements = {
            "Rename service:":self.edit_input_service,
            "Rename URL:":self.edit_input_url,
            "Rename login:":self.edit_input_login,
            "Rename password:":self.edit_input_password
        }

        for edit_input_name, edit_input_elements in edit_input_layout_elements.items():
            self.edit_input_layout.addRow(edit_input_name, edit_input_elements)

        self.edit_password_layout.addWidget(message)
        self.edit_password_layout.addLayout(self.edit_input_layout)
        self.edit_password_layout.addWidget(buttons)

        self.setLayout(self.edit_password_layout)
        
        self.show()
        
    def accept(self):
        self._save_edit()

    def _save_edit(self):
        # Получаем новые данные
        service  = self.edit_input_service.text().strip()
        url      = self.edit_input_url.text().strip()
        login    = self.edit_input_login.text().strip()
        password = self.edit_input_password.text().strip()

        # write new data
        data = {
            "service": service,
            "url": url,
            "login": login,
            "password": password,
        }

        self.data_edit_password.emit(data) #send new data
        self.finished.emit()               #finish thread
        super().accept()
