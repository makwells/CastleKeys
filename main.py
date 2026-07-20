# main.py

import sys
from PyQt6.QtWidgets import QApplication
from src.views.main_window import MainWindow
from src.views.Dialogs.Create_New_Password import CreateNewPassword
from src.views.Dialogs.edit_password import Edit_Password
from src.controllers.main_controller import MainController
from src.database import *

class Password_Manager:
    
    version = 0.1
    program_name = "CastleKeys"
    author = "makwells"
    project = "https://github.com/makwells/CastleKeys"

    def __init__(self):
        with open("src/assets/styles/main_styles.qss", "r") as styles_file:
            self.style = styles_file.read()

        self.PM()
        print(self.version)

    def PM(self):

        app = QApplication(sys.argv)
        
        view = MainWindow()
        controller = MainController(view)

        view.show()

        app.setStyleSheet(self.style)

        sys.exit(app.exec())

if __name__ == "__main__":
    Password_Manager()