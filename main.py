"""
PM -

"""


import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFontDatabase
from src.views.main_window import MainWindow
from src.controllers.main_controller import MainController

class Password_Manager:
    
    version = 0.1
    program_name = "PM"
    author = "makwells"
    project = "https://github.com/makwells/"

    def __init__(self):
        with open("src/assets/main_styles.qss", "r") as styles_file:
            self.style = styles_file.read()

        self.PM()
        print(self.version)

    def PM(self):

        app = QApplication(sys.argv)
        
        view = MainWindow()
        controller = MainController(view)

        view.show()

        # QFontDatabase.addApplicationFont("src/assets/fonts/FiraCode.ttf")

        app.setStyleSheet(self.style)

        sys.exit(app.exec())

if __name__ == "__main__":
    Password_Manager()