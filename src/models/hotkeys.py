from PySide6.QtGui import QKeySequence, QShortcut


def HotKeys(self):
    def selected_action(action):
        page = self._pages.passwords_page

        if (
            self._pages.currentWidget() is page.passwords_page_widget
            and page.selected_password_id is not None
            and not page.main_password_information_widget.isHidden()
        ):
            action()

    def focus_search():
        page = self._pages.passwords_page

        self._pages.setCurrentWidget(page.passwords_page_widget)
        page.back_to_passwords()

        self._view.topbar.search_le.setFocus()
        self._view.topbar.search_le.selectAll()

    actions = {
        "new_password": (
            "Ctrl+N",
            self._add_entry_clicked,
        ),
        "edit_password": (
            "Ctrl+E",
            lambda: selected_action(self._edit_password_clicked),
        ),
        "del_password": (
            "Ctrl+Backspace",
            lambda: selected_action(self._del_password_clicked),
        ),
        "hide_password": (
            "Ctrl+G",
            lambda: selected_action(self.hide),
        ),
        "settings": (
            "Ctrl+I",
            self._setting_clicked,
        ),
        "main_menu": (
            "Escape",
            self.main_menu,
        ),
        "search": (
            "Ctrl+F",
            focus_search,
        ),
    }

    self.shortcuts = {}
    config = self.config.get("hotkeys", {})

    for name, (default, callback) in actions.items():
        sequence = config.get(name, default)

        if sequence:
            shortcut = QShortcut(
                QKeySequence(sequence),
                self._view,
            )
            shortcut.activated.connect(callback)
            self.shortcuts[name] = shortcut