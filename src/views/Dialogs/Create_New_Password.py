# create_new_password.py
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from src.database import *
from src.setuplogger import setup_logger

class CreateNewPassword(QDialog):
    password_created = pyqtSignal(object)
    data_created_password = pyqtSignal(dict)
    finished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        with open("src/assets/styles/dialog_styles.qss", "r", encoding="utf-8") as styles_file:
            style = styles_file.read()
            self.setStyleSheet(style)

        self.setWindowTitle("New password")
        self.setFixedSize(400, 400)
        self.new_password_ui()
        
    def new_password_ui(self):
        self.new_password_layout = QVBoxLayout()
        self.new_password_input_layout = QFormLayout()
        self.new_password_input_layout.setFormAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.new_password_input_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        self.new_password_input_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)

        message = QLabel("Create new password")
        message.setStyleSheet("font-weight: bold;")
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.input_service = QLineEdit()
        self.input_service.setPlaceholderText("example.com")
        self.input_url = QLineEdit()
        self.input_url.setPlaceholderText("https://example.com/")
        self.input_login = QLineEdit()
        self.input_login.setPlaceholderText("example@gmail.com")
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("example12345")

        # <-- Подключаем real-time сохранение к каждому полю
        self.input_service.textChanged.connect(self._on_realtime_save)
        self.input_url.textChanged.connect(self._on_realtime_save)
        self.input_login.textChanged.connect(self._on_realtime_save)
        self.input_password.textChanged.connect(self._on_realtime_save)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept) 
        buttons.rejected.connect(self.reject) 

        new_password_input_layout_elements = {
            "Service:": self.input_service,
            "URL:": self.input_url,
            "Login:": self.input_login,
            "Password:": self.input_password
        }

        for new_input_name, new_input_elements in new_password_input_layout_elements.items():
            self.new_password_input_layout.addRow(new_input_name, new_input_elements)
        
        self.new_password_layout.addWidget(message)
        self.new_password_layout.addLayout(self.new_password_input_layout)
        self.new_password_layout.addWidget(buttons)
        self.setLayout(self.new_password_layout)
        self.show()

    def _on_realtime_save(self):
        """Отправляет данные в контроллер при каждом изменении текста"""
        data = {
            "service": self.input_service.text().strip(),
            "url": self.input_url.text().strip(),
            "login": self.input_login.text().strip(),
            "password": self.input_password.text().strip(),
        }
        # Эмитим сигнал, если хотя бы одно поле не пустое
        if any(data.values()):
            self.data_created_password.emit(data)

    def accept(self):
        # Так как сохранение идет в реальном времени, просто закрываем окно
        super().accept() 

    def reject(self):
        super().reject()