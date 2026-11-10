#mainMenu_page.py
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from src.setuplogger import *
from src.config_manager import ConfigManager


class Main_menu_page(QObject):
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager() # init configuration
        self.main_menu_page()

    def main_menu_page(self):
        self.config = self.config_manager.load_config()

        self.main_menu_widget = QWidget()
        self.main_menu_widget.setObjectName("RightWorkspace")
        self.main_menu_layout = QVBoxLayout(self.main_menu_widget)

        self.welcome_logo = QLabel()
        self.welcome_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.welcome_text = QLabel("")
        
        welcome_logo_path = self.config["view"]["welcome_logo"]
        pixmap = QPixmap(self.config_manager.get_resource_path(welcome_logo_path))
                
                
        if not pixmap.isNull():
            # Масштабируем до 200x200 с сохранением пропорций и сглаживанием
            scaled_pixmap = pixmap.scaled(
            self.config["view"]["welcome_logo_width"], self.config["view"]["welcome_logo_height"], 
                        Qt.AspectRatioMode.KeepAspectRatio, 
                        Qt.TransformationMode.SmoothTransformation
            )
            self.welcome_logo.setPixmap(scaled_pixmap)
        else:
            logger.warning("Logo image not found! Showing placeholder text.")

        self.main_menu_layout.addStretch()
        self.main_menu_layout.addWidget(self.welcome_logo)
        self.main_menu_layout.addStretch()
        