# main.py
from PySide6.QtWidgets import QApplication

from src.setuplogger import logger

from src.views import MainWindow
from src.views import Settings

from src.controllers import MainController
from src.controllers import SettingsController

from src.models import backups

import sys

class CastleKeys:
    program_name = "CastleKeys"
    author = "makwells"
    project = "https://github.com/makwells/CastleKeys"

    def __init__(self):

        logger.success("The application has started")

        self.castlekeys()

    def castlekeys(self):
        backups.backup_timer() # Run backup timer
        logger.debug("Backup timer is running!")

        cleaned_args = [arg for arg in sys.argv if not arg.startswith("-psn")]

        app = QApplication(cleaned_args)

        view = MainWindow()
        settings = Settings()

        controller = MainController(view)
        settings_controller = SettingsController(settings, view)

        settings.hide()
        view.show()
        sys.exit(app.exec())

if __name__ == "__main__":
    CastleKeys()