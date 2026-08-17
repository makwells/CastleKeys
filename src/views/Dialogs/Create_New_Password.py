# create_new_password.py
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from src.setuplogger import logger
from src.config_manager import ConfigManager

class CreateNewPassword(QDialog):
    #signals
    password_created = Signal(object)
    data_created_password = Signal(dict)
    finished = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        #Dialog styles 
        styles_path = ConfigManager.get_resource_path("src/assets/styles/dialog_styles.qss")
        with open(styles_path, "r", encoding="utf-8") as styles_file:
            self.setStyleSheet(styles_file.read())
            logger.success(f"Styles for the {__name__} window have been loaded")

        self.new_password_ui() #start ui
        
    def new_password_ui(self): #ui
        self.setWindowTitle("New password") #title
        self.setFixedSize(400, 400)         #window size

        self.new_password_layout = QVBoxLayout() #main window layout
        self.new_password_input_layout = QFormLayout() #second window layout
        #settings second window layout
        self.new_password_input_layout.setFormAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.new_password_input_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        self.new_password_input_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)

        #message
        message = QLabel("Create new password") 
        message.setStyleSheet("font-weight: bold;") #message font bold parameter
        message.setAlignment(Qt.AlignmentFlag.AlignCenter) #message aligment

        #service input field 
        self.input_service = QLineEdit() 
        self.input_service.setPlaceholderText("example.com")

        #url input field 
        self.input_url = QLineEdit() 
        self.input_url.setPlaceholderText("https://example.com/")

        #login input field
        self.input_login = QLineEdit() 
        self.input_login.setPlaceholderText("example@gmail.com")

        #password input field
        self.input_password = QLineEdit() 
        self.input_password.setPlaceholderText("example12345")

        #realtime tracking of text changes in input fields 
        self.input_service.textChanged.connect(self._on_realtime_save)
        self.input_url.textChanged.connect(self._on_realtime_save)
        self.input_login.textChanged.connect(self._on_realtime_save)
        self.input_password.textChanged.connect(self._on_realtime_save)


        # buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept) 
        buttons.rejected.connect(self.reject) 

        #interface elements for the second layout
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

    def _on_realtime_save(self):
        #send data to the controller whenever the text changes
        data = {
            "service": self.input_service.text().strip(),
            "url": self.input_url.text().strip(),
            "login": self.input_login.text().strip(),
            "password": self.input_password.text().strip(),
        }
        #send data
        if any(data.values()):
            self.data_created_password.emit(data)

    def accept(self):
        #close window 
        super().accept() 

    #close the window without entering a new password
    def reject(self):
        super().reject()