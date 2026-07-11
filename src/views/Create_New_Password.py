# Create_New_Password.py
import sys
from PyQt6.QtWidgets import *
# from ..controllers.main_controller import *

class CreateNewPassword(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Create new password")
        self.setFixedSize(300, 150)

        self._new_password_ui()

    def _new_password_ui(self):
        layout = QVBoxLayout()
        message = QLabel(f"Create new password")
        
        enter_password = QLineEdit()

        # Add native OK / Cancel button groups
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept) # Triggers QDialog built-in accept state
        buttons.rejected.connect(self.reject) # Triggers QDialog built-in reject state
        
        layout.addWidget(message)
        layout.addWidget(enter_password)
        layout.addWidget(buttons)
    
        self.setLayout(layout)

        self.show()