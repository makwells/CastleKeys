# main.py
from PyQt6.QtWidgets import QApplication

from src.views import MainWindow
from src.views import Settings

from src.controllers import MainController
from src.controllers import SettingsController

from src import database
from src.setuplogger import logger

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
        settings = Settings()

        controller = MainController(view)
        settings_controller = SettingsController(settings, view)

        settings.hide()
        view.show()
        sys.exit(app.exec())

if __name__ == "__main__":
    CastleKeys()