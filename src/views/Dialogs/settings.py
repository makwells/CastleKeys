from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from src.database import *

from src.config_manager import ConfigManager


class Settings(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        styles_path = ConfigManager.get_resource_path("src/assets/styles/settings_styles.qss")
        with open(styles_path, "r", encoding="utf-8") as styles_file:
            self.setStyleSheet(styles_file.read())

        config_path = ConfigManager.get_resource_path("config.toml")
        with open(config_path, "r", encoding="utf-8") as config_file:
            self.config = toml.load(config_file)

        self.settings_ui()
    
    def settings_ui(self):
        def add_separator():
            line = QFrame()
            line.setFrameShape(QFrame.Shape.HLine)
            line.setFrameShadow(QFrame.Shadow.Sunken)
            form_layout.addRow(line)

        self.setWindowTitle("Settings")
        self.resize(800, 600)

        main_layout = QVBoxLayout(self)

        content_widget = QWidget()
        form_layout = QFormLayout(content_widget)


        view_lb = QLabel("View")
        theme_combo = QComboBox()
        font_family_lb = QLineEdit()
        animations_cb = QCheckBox()
        self.startup_animations_cb = QCheckBox()
        self.startup_animations_cb.setChecked(self.config["view"]["window_startup_animations"])
        language_combo = QComboBox()
        notifications_cb = QCheckBox()
        welcome_logo_le = QLineEdit()
        welcome_logo_width_le = QLineEdit()
        welcome_logo_height_le = QLineEdit()


        storage_lb = QLabel("Storage")
        autosave_combo = QCheckBox()
        database_dir_le = QLineEdit()
        backup_dir_le = QLineEdit()
        backup_cb = QCheckBox()
        backup_time_combo = QComboBox()

        privacy_lb = QLabel("Privacy")
        auto_hide_passwords_combo = QCheckBox()
        confirm_password_cb = QCheckBox()


        form_layout.addWidget(view_lb)
        form_layout.addRow(QLabel(f"Theme:"), theme_combo)
        form_layout.addRow(QLabel(f"Font Family:"), font_family_lb)
        form_layout.addRow(QLabel(f"Animations:"), animations_cb)
        form_layout.addRow(QLabel(f"Start animations:"), self.startup_animations_cb)
        form_layout.addRow(QLabel(f"Language:"), language_combo)
        form_layout.addRow(QLabel(f"Notifications:"), notifications_cb)
        form_layout.addRow(QLabel(f"Welcome logo:"), welcome_logo_le)
        form_layout.addRow(QLabel(f"Welcome logo width:"), welcome_logo_width_le)
        form_layout.addRow(QLabel(f"Welcome logo height:"), welcome_logo_height_le)
        add_separator()
        form_layout.addWidget(storage_lb)
        form_layout.addRow(QLabel("AutoSave"), autosave_combo)
        form_layout.addRow(QLabel("Database dir"), database_dir_le)
        form_layout.addRow(QLabel("Download dir"), backup_dir_le)
        form_layout.addRow(QLabel("Backup"), backup_cb)
        form_layout.addRow(QLabel("Backup time"), backup_time_combo)
        add_separator()
        form_layout.addWidget(privacy_lb)
        form_layout.addRow(QLabel("Auto hide passwords"), auto_hide_passwords_combo)
        form_layout.addRow(QLabel("Confirm password"), confirm_password_cb)



        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(content_widget)

        main_layout.addWidget(scroll)
        
        close_btn = QPushButton("Сохранить и закрыть")
        close_btn.clicked.connect(self.accept)
        main_layout.addWidget(close_btn)

        self.show()