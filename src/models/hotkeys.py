#hotkeys.py
from PySide6.QtGui import *

def HotKeys(self): 
    hotkeys = {
        "new_password":  self.config["hotkeys"].get("new_password", "Ctrl+N"),
        "edit_password": self.config["hotkeys"].get("edit_password", "Ctrl+E"),
        "del_password": self.config["hotkeys"].get("del_password", "Ctrl+Backspace"),
        "hide_password": self.config["hotkeys"].get("hide_password", "Ctrl+G"),
        "settings": self.config["hotkeys"].get("settings", "Ctrl+I"),
        "main_menu": self.config["hotkeys"].get("main_menu", "Escape")
    }

    if hotkeys["new_password"]:
        self.shortcut_new = QShortcut(QKeySequence(hotkeys["new_password"]), self._view)
        self.shortcut_new.activated.connect(self._new_password_clicked)

    if hotkeys["edit_password"]:
        self.shortcut_edit = QShortcut(QKeySequence(hotkeys["edit_password"]), self._view)
        self.shortcut_edit.activated.connect(self._edit_password_clicked)
    
    if hotkeys["del_password"]:
        self.shortcut_del = QShortcut(QKeySequence(hotkeys["del_password"]), self._view)
        self.shortcut_del.activated.connect(lambda: self._del_password_clicked(self._view.tree_view))

    if hotkeys["hide_password"]:
        self.shortcut_hide = QShortcut(QKeySequence(hotkeys["hide_password"]), self._view)
        self.shortcut_hide.activated.connect(self.hide)

    if hotkeys["settings"]:
        self.shortcut_settings = QShortcut(QKeySequence(hotkeys["settings"]), self._view)
        self.shortcut_settings.activated.connect(self._setting_clicked)

    if hotkeys["main_menu"]:
        self.shortcut_main_menu = QShortcut(QKeySequence(hotkeys["main_menu"]), self._view)
        self.shortcut_main_menu.activated.connect(self.main_menu)
