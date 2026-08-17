#toolbar.py 
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

class MenuBar:
    def __init__(self):
        ...

    def menubar_elements(self):
        self.menu_bar = self.menuBar()

        file_menu = self.menu_bar.addMenu("Файл")

        new_password = QAction("New password", self)
        new_password.addAction()
        new_tag = QAction("New tag", self)
        new_database = QAction("New database", self)

        import_database = QAction("Import database", self)
        export_database = QAction("Export database", self)

        settings = QAction("Settings", self)

        file_menu.addAction(new_password)
        file_menu.addAction(new_tag)
        file_menu.addAction(new_database)
        file_menu.addSeparator()
        file_menu.addAction(import_database)
        file_menu.addAction(export_database)
        file_menu.addSeparator()
        file_menu.addAction(settings)





