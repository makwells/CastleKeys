#Pages.py
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from src.setuplogger import *
from src.views.ui.notifications.notifications_window import *

class MenuBar:
    def __init__(self):
        self.init_menubar()

    def init_menubar(self): #menu bar
        self.menu = QMenuBar() #widget menu bar

        # #file menu
        # file_menu = self.menu.addMenu("File") 
        # #file menu elements
        # self.new_password_menu = QAction("New password", self)
        # self.new_tag_menu = QAction("New tag", self)
        # self.new_database_menu = QAction("New database", self)

        # self.edit_password_menu = QAction("Edit menu", self)
        # self.edit_database_menu = QAction("Edit database", self)

        # self.import_database_menu = QAction("Import database", self)
        # self.export_database_menu = QAction("Export database", self)
        # self.settings_menu = QAction("Settings", self)
        # #file menu add elements
        # file_menu.addAction(self.new_password_menu)
        # file_menu.addAction(self.new_tag_menu)
        # file_menu.addAction(self.new_database_menu)
        # file_menu.addSeparator()
        # file_menu.addAction(self.edit_password_menu)
        # file_menu.addAction(self.edit_database_menu)
        # file_menu.addSeparator()
        # file_menu.addAction(self.import_database_menu)
        # file_menu.addAction(self.export_database_menu)
        # file_menu.addSeparator()
        # file_menu.addAction(self.settings_menu)

        # #view menu 
        # view_menu = self.menu.addMenu("View")
        # #view menu elements
        # change_theme = QAction("Change theme", self)
        # #view menu add elemets
        # view_menu.addAction(change_theme)
