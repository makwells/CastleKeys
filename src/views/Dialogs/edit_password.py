#edit_passwords.py
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from src.setuplogger import logger
from src.config_manager import ConfigManager
from src.models import generate_password

class Edit_Password(QDialog):

    data_edit_password = Signal(object)
    finished = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        dialog_style = ConfigManager.get_dialog_style()
        self.setStyleSheet(dialog_style)

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


        #generate_random_password button 
        self.generate_password = QPushButton("Generate random password")
        self.generate_password.setFixedSize(300, 30)
        self.generate_password.clicked.connect(self.generator_random_password)

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
        self.edit_password_layout.addWidget(self.generate_password, alignment=Qt.AlignHCenter)

        self.setLayout(self.edit_password_layout)
        
    def accept(self):
        self._save_edit()

    def generator_random_password(self):
        _gen_password = generate_password.generate_random_password(15)
        self.edit_input_password.setText(_gen_password)

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
