from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from src.database import *

class Edit_Password(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # self._controller_clicked = self._controller._on_category_clicked

        with open("src/assets/styles/dialog_styles.qss", "r") as styles_file:
            style = styles_file.read()

        self.setStyleSheet(style)

        self.setWindowTitle("Edit password")
        self.setFixedSize(400, 400)

        self.edit_password_ui()

    
    def edit_password_ui(self):
        self.edit_password_layout = QVBoxLayout()
        message = QLabel(f"Edit password")
        message.setStyleSheet("font-weight: bold;")
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        
        self.edit_label_service = QLabel("Rename service:")
        self.edit_input_service = QLineEdit()
        self.edit_input_service.setPlaceholderText("example.com")
        self.edit_label_login = QLabel("New login:")
        self.edit_input_login = QLineEdit()
        self.edit_input_login.setPlaceholderText("example@gmail.com")
        self.edit_label_password = QLabel("New password:")
        self.edit_input_password = QLineEdit()
        self.edit_input_password.setPlaceholderText("example123456789")
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept) # Triggers QDialog built-in accept state
        buttons.rejected.connect(self.reject) # Triggers QDialog built-in reject state
        
        self.edit_password_layout.addWidget(message)
        self.edit_password_layout.addWidget(self.edit_label_service)
        self.edit_password_layout.addWidget(self.edit_input_service)
        self.edit_password_layout.addWidget(self.edit_label_login)
        self.edit_password_layout.addWidget(self.edit_input_login)
        self.edit_password_layout.addWidget(self.edit_label_password)
        self.edit_password_layout.addWidget(self.edit_input_password)
        self.edit_password_layout.addWidget(buttons)

        self.setLayout(self.edit_password_layout)

        self.show()
    
    def accept(self):
        self.edit_password(self.edit_input_service, self.edit_input_login, self.edit_input_password)
        super().accept
    
    def edit_password(self, service, login, password):
        ...