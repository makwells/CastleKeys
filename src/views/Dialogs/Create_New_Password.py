# create_new_password.py
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from src.setuplogger import logger
from src.config_manager import ConfigManager
from src.models import generate_password

class CreateNewPassword(QDialog):
    #signals
    password_created = Signal(object)
    data_created_password = Signal(dict)
    finished = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        #styles
        config_manager = ConfigManager()
        dialog_style = config_manager.get_dialog_style()
        self.setStyleSheet(dialog_style)
        logger.debug(f"Styles for {__name__} has been loaded")

        self.new_password_window() #start ui
        
    def new_password_window(self): #ui
        logger.success("The new password creation dialog box has been loaded")
        self.setWindowTitle("New password") #title
        self.setFixedSize(400, 400) #window size

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

        #generate_random_password button 
        self.generate_password = QPushButton("Generate random password")
        self.generate_password.setFixedSize(300, 30)
        self.generate_password.clicked.connect(self.generator_random_password)

        # buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept) 
        buttons.rejected.connect(self.reject) 
        
        self.new_password_layout.addWidget(message)
        self.new_password_input_layout.addRow("Service:", self.input_service)
        self.new_password_input_layout.addRow("URL:", self.input_url)
        self.new_password_input_layout.addRow("Login:", self.input_login)
        self.new_password_input_layout.addRow("Password:", self.input_password)

        self.new_password_layout.addLayout(self.new_password_input_layout)
        self.new_password_layout.addWidget(self.generate_password, alignment=Qt.AlignHCenter)
        self.new_password_layout.addWidget(buttons)
        self.setLayout(self.new_password_layout)


    def generator_random_password(self):
        _gen_password = generate_password.generate_random_password()
        self.input_password.setText(_gen_password)

    def _on_realtime_save(self):
        #send data to the controller whenever the text changes
        self.create_new_password_data = {
            "service": self.input_service.text().strip(),
            "url": self.input_url.text().strip(),
            "login": self.input_login.text().strip(),
            "password": self.input_password.text().strip(),
        }

    def accept(self):
        #close window 
        logger.debug("Password")

        #data sent to main controller 
        logger.debug("data sent to main_controller.py")
        try:        
            self.data_created_password.emit(self.create_new_password_data)
        except Exception as e:
            logger.warning("Data is empty. The password was not added!")
    
        #close windowm
        super().accept()  
        

    #close the window without entering a new password
    def reject(self):
        super().reject()