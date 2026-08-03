from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from src.database import *

class Settings(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        with open("src/assets/styles/dialog_styles.qss", "r") as styles_file:
            style = styles_file.read()

        self.setStyleSheet(style)
        self.settings_ui()
    
    def settings_ui(self):
        self.setWindowTitle("Settings")
        self.resize(800, 600)

        self.main_block = QVBoxLayout()

        self.app_block = QFormLayout()

        # Language
        self.language_combo = QComboBox()
        languages = ["en", "ru"]
        self.language_combo.addItems(languages)

        # self.language_combo.currentIndexChanged.connect(self.language_change)

        # Theme
        self.theme_combo = QComboBox()
        themes = ["Dark", "Light"]
        self.theme_combo.addItems(themes)


        # Font-Family
        self.font_family_combo = QComboBox()
        fonts = []
        self.font_family_combo.addItems(fonts)


        # Font-Size
        self.font_size_le = QLineEdit()
        self.font_size_le.setPlaceholderText("12pt")


        # Animations 
        self.animations_cb = QCheckBox()
        self.animations_cb.setChecked(True)

        app_block_parameters = {
            "Language:":self.language_combo, 
            "Theme:":self.theme_combo,
            "Font-Family:":self.font_family_combo,
            "Font-Size:":self.font_size_le,
            "Animations:":self.animations_cb
        }
        for app_block_name, app_block_element in app_block_parameters.items():
            self.app_block.addRow(QLabel(app_block_name), app_block_element) 


        self.storage_block = QFormLayout()


        #Path to passwords
        self.path_to_passwords_le = QLineEdit()
        self.path_to_passwords_le.setPlaceholderText(".Passwords")


        # AutoSave
        self.auto_save_cb = QCheckBox()
        self.auto_save_cb.setChecked(True)

        storage_block_parameters = {
            "Path to passwords:":self.path_to_passwords_le,
            "AutoSave:":self.auto_save_cb
        }

        for storage_block_name, storage_block_element in storage_block_parameters.items():
            self.storage_block.addRow(QLabel(storage_block_name), storage_block_element)

            
        self.main_block.addLayout(self.app_block)
        self.main_block.addLayout(self.storage_block)
        self.setLayout(self.main_block)
        self.show()


    # def language_change(self, index):
    #         # Получаем выбранный текст
    #         selected_text = self.language_combo.currentText()
    #         # Обновляем текст на экране
    #         self.label_result.setText(f"Текущий выбор: {selected_text} (индекс: {index})")
    #         print(f"Пользователь выбрал параметр: {selected_text}")