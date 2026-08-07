# main.py
from PyQt6.QtWidgets import QApplication
from src.views.main_window import MainWindow
from src.views.Dialogs.create_new_password import CreateNewPassword
from src.views.Dialogs.edit_password import Edit_Password
from src.controllers.main_controller import MainController

from src.database import *
from src.setuplogger import setup_logger
import sys


class CastleKeys:
    
    version = 0.1
    program_name = "CastleKeys"
    author = "makwells"
    project = "https://github.com/makwells/CastleKeys"

    def __init__(self):
        logger.success("The application has started.")

        self.castlekeys()

    def castlekeys(self):

        app = QApplication(sys.argv)
        
        view = MainWindow()
        controller = MainController(view)

        view.show()
        sys.exit(app.exec())

if __name__ == "__main__":
    CastleKeys()