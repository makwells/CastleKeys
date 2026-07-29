# main.py

import sys
from PyQt6.QtWidgets import QApplication
from src.views.main_window import MainWindow
from src.views.Dialogs.create_new_password import CreateNewPassword
from src.views.Dialogs.edit_password import Edit_Password
from src.controllers.main_controller import MainController

from src.database import *
from src.setuplogger import setup_logger

class CastleKeys:
    
    version = 0.1
    program_name = "CastleKeys"
    author = "makwells"
    project = "https://github.com/makwells/CastleKeys"

    def __init__(self):
        setup_logger()
        logger.success("The application has started.")

        with open("src/assets/styles/main_styles.qss", "r") as styles_file:
            self.style = styles_file.read()

        self.castlekeys()
        print(self.version)

    def castlekeys(self):

        app = QApplication(sys.argv)
        try:
            app.setStyleSheet(self.style)
            logger.debug("Styles for the main window have been loaded.")
        except Exception:
            ...
        
        view = MainWindow()
        controller = MainController(view)

        view.show()
        sys.exit(app.exec())

if __name__ == "__main__":
    CastleKeys()