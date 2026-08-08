#main_controller.py
from ..views.Dialogs.create_new_password import CreateNewPassword
from ..views.Dialogs.settings import Settings
from ..views.Dialogs.edit_password import Edit_Password

from ..models.db_info import Database_info
from src.views.icons import icons_set_color


from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from ..database import *
from ..setuplogger import setup_logger


class MainController():
    def __init__(self, view):
        with open("config.toml", "r", encoding="utf-8") as config_file:
            self.config = toml.load(config_file)

        self._view  = view      #MainWindow

        self.service_name_ = None
        self.login_ = None
        self.url_ = None
        self.password_ = None
        self.current_password = None
        self._view.hide_password_btn_state = not self._view.hide_password_btn_state

        self._connect_signals() #Signals
        self.HotKeys()

    def _connect_signals(self):
        
        self._view.tree_view.clicked.connect(self._on_category_clicked)               #tree select category
        self._view.new_password_btn.clicked.connect(self._new_password_clicked)       #new password button
        self._view.settings_btn.clicked.connect(self._setting_clicked)                #settings button
        self._view.search_btn.clicked.connect(self._search_clicked)
        self._view.edit_password_btn.clicked.connect(self._edit_password_clicked)     #edit password button 
        self._view.hide_password_btn.clicked.connect(self.hide)
        self._view.del_password_btn.clicked.connect(self._del_password_clicked)       #del password button 

        # TODO Нужно блокировать окно программы, когда открыто диалоговое окно, чтобы нельзя было открыть одновремено несколько окон добавления пароля или окон редактрирования. 

    def _on_category_clicked(self, index): #select category

        self.item = self._view.tree_model.itemFromIndex(index)
        item_name = self.item.text()                                          #get text
        self._view.title.setText(f"{item_name}".upper())                      #change title
        

        if self.item == self._view.root_item: # если выбран заголовок в пункте меню, то скрывать значения сервиса логина и пароля, вызвав функцию для просмотра информации о бд
            self._view.title.hide()
            self._view.service_lb.hide()
            self._view.url_lb.hide()
            self._view.login_lb.hide()
            self._view.password_lb.hide()
            self._view.creation_date_lb.hide()
            self._view.description_lb.hide()
            self._view.description.hide()
            self._view.hide_password_btn.hide()
            self._view.edit_password_btn.hide()
            self._view.del_password_btn.hide()

            self.db_information()
            return

        else: # если выбрано что-то иное то показывать
            logger.debug(f"Tree element selected: {item_name}")
            self._view.title.show()
            self._view.service_lb.show()
            self._view.url_lb.show()
            self._view.login_lb.show()
            self._view.password_lb.show()
            self._view.creation_date_lb.show()
            self._view.description_lb.show()
            self._view.description.show()
            self._view.hide_password_btn.show()
            self._view.edit_password_btn.show()
            self._view.del_password_btn.show()
            self._view.welcome_logo.hide()


            self._view.db_size_lb.hide()
            self._view.db_creation_date.hide()
            self._view.path_to_db.hide()
            self._view.db_count_passwords.hide()
            self._view.db_count_dublicate.hide()
            self._view.db_login.hide()
            self._view.db_password.hide()

        self.service_name_ = self.item.text()
        self.login_ = self.item.data(Qt.ItemDataRole.UserRole + 1)
        self.url_ = self.item.data(Qt.ItemDataRole.UserRole + 2)
        self.password_ = self.item.data(Qt.ItemDataRole.UserRole + 3)
        self.date_ = self.item.data(Qt.ItemDataRole.UserRole + 4)
        self.description_ = self.item.data(Qt.ItemDataRole.UserRole + 5)

        self._view.service_lb.setText(f"Service: {self.service_name_}")
        self._view.login_lb.setText(f"Login: {self.login_}")
        self._view.url_lb.setText(f"URL: {self.url_}")
        self._view.password_lb.setText(f"Password: {self.password_}")
        self._view.creation_date_lb.setText(f"Creation date: {self.date_}")

        self.current_password = self._view.password_lb.text()
        self.password_length = len(self.current_password)
        self.hide_password = "*" * self.password_length
            

    def _new_password_clicked(self): #add new password
        logger.debug("New button clicked")

        self.new_menu = CreateNewPassword(self._view)

        self._new_password_saved = False 
        self._new_tree_item = None
        self._current_new_id = None

        self.new_menu.data_created_password.connect(self._update_ui_new_password_realtime)

    def _update_ui_new_password_realtime(self, data: dict):
        get_service = data.get("service", "")
        get_url = data.get("url", "")
        get_login = data.get("login", "")
        get_password = data.get("password", "")

        if not self._new_password_saved:
            new_id = add_password(
                service=get_service,
                url=get_url,
                login=get_login,
                password=get_password
            )

            if new_id and new_id != -1:
                self._new_password_saved = True
                self._current_new_id = new_id
                
                from datetime import datetime
                current_date = datetime.now().strftime("%Y-%m-%d %H:%M")

                # Создаем элемент в дереве
                service_item = QStandardItem(get_service or "New Entry")
                service_item.setData(self._current_new_id, Qt.ItemDataRole.UserRole)
                service_item.setData(get_login, Qt.ItemDataRole.UserRole + 1)
                service_item.setData(get_url, Qt.ItemDataRole.UserRole + 2)
                service_item.setData(get_password, Qt.ItemDataRole.UserRole + 3)
                service_item.setData(current_date, Qt.ItemDataRole.UserRole + 4) # Ставим текущую дату
                service_item.setData("", Qt.ItemDataRole.UserRole + 5)           # Пустое описание

                self._view.root_item.appendRow(service_item)
                self._new_tree_item = service_item
                logger.debug(f"New password created in DB with ID {self._current_new_id}")

        elif self._new_password_saved and self._current_new_id is not None:
            success = update_password(
                password_id=self._current_new_id,
                service=get_service,
                url=get_url,
                login=get_login,
                password=get_password
            )
            
            if success and self._new_tree_item:
                self._new_tree_item.setText(get_service or "New Entry")
                self._new_tree_item.setData(get_login, Qt.ItemDataRole.UserRole + 1)
                self._new_tree_item.setData(get_url, Qt.ItemDataRole.UserRole + 2)
                self._new_tree_item.setData(get_password, Qt.ItemDataRole.UserRole + 3)
                logger.debug(f"Password ID {self._current_new_id} updated in DB and UI") 
 
    def _edit_password_clicked(self): #edit password
        #open the child window to edit a password
        logger.debug("Edit button clicked")
        
        self.edit_menu = Edit_Password()
        # self.edit_menu.exec()
        
        get_service = self.service_name_
        get_url = self.url_
        get_login = self.login_
        get_password = self.password_

        # заполнять холдертекст старыми данными
        self.edit_menu.edit_input_service.setPlaceholderText(get_service)
        self.edit_menu.edit_input_login.setPlaceholderText(get_login)
        self.edit_menu.edit_input_url.setPlaceholderText(get_url)
        self.edit_menu.edit_input_password.setPlaceholderText(get_password)

        self.edit_menu.data_edit_password.connect(self.update_ui_edited)
    
    def update_ui_edited(self, data:dict): #update edited passwords
        #get edited password 
        new_service  = data.get("service") or self.service_name_
        new_url      = data.get("url") or self.url_
        new_login    = data.get("login") or self.login_
        new_password = data.get("password") or self.password_
        
        if new_service != "": logger.debug(f"Received updated service data: {new_service}")
        if new_url != "": logger.debug(f"Received updated url data: {new_url}")
        if new_login != "": logger.debug(f"Received updated login data: {new_login}")
        if new_password != "": logger.debug(f"Received updated password data: {new_password}")


        #change in db
        success = update_password(
            password_id=self._view.entry_id,
            service=new_service,
            url=new_url,
            login=new_login,
            password=new_password
        )
        if success:
            #change in ui
            self._view.service_lb.setText(f"Service: {new_service}") 
            self._view.url_lb.setText(f"URL: {new_url}")
            self._view.login_lb.setText(f"Login: {new_login}")
            self._view.password_lb.setText(f"Password: {new_password}")

            self.service_name_ = new_service
            self.url_ = new_url
            self.login_ = new_login
            self.password_ = new_password

            self.item.setText(self.service_name_)                     # заголовок в дереве
            self._view.title.setText(f"{self.service_name_}".upper()) #заголовок в right_workspace
            
    def _del_password_clicked(self, tree_view): #del password
        logger.debug("Del button clicked")
        # Получаем индекс выбранного элемента
        current_index = self._view.tree_view.currentIndex()
        
        if not current_index.isValid():
            return

        model = self._view.tree_view.model() 
        row = current_index.row()
        parent_index = current_index.parent()

        # Находим индекс первой колонки (0) для выделенной строки
        first_column_index = model.index(row, 0, parent_index)
        
        # Извлекаем спрятанный ID базы данных из роли UserRole
        db_id = model.data(first_column_index, Qt.ItemDataRole.UserRole)

        if db_id is None:
            logger.error("The database identifier is missing from the interface element!")
            return

        # Удаления из базы данных
        if delete_password(db_id):
            # Если из файла базы данных удалено, удаляем строку из интерфейса
            model.removeRow(row, parent_index)
            logger.success(f"The row with ID {db_id} has been removed from the interface.")
    
    def _setting_clicked(self): #settings
        #open the child window for application settings
        logger.debug("Settings button clicked")
        Settings(self._view)

    def _search_clicked(self): #seach
        logger.debug("Search button clicked")

    def db_information(self): #database information
        logger.debug("db_infromation clicked")
        self._view.db_size_lb.show()
        self._view.db_creation_date.show()
        self._view.path_to_db.show()
        self._view.db_count_passwords.show()
        self._view.db_count_dublicate.show()
        self._view.db_login.show()
        self._view.db_password.show()
    
    def hide(self, checked=None): #hide passwords

        icon_size = QSize(24, 24)
    
        if not self._view.hide_password_btn_state:
            self._view.password_lb.setText("Password: " + self.hide_password) 
            self._view.hide_password_btn.setText("")
            self._view.hide_password_icon = icons_set_color("hide.svg", "#D3D3D3", icon_size)
            self._view.hide_password_btn.setIcon(self._view.hide_password_icon)
            self._view.hide_password_btn.setIconSize(icon_size)

            self._view.hide_password_btn_state = True
            logger.debug("Password hidden")
        else:
            self._view.password_lb.setText(self.current_password)
            self._view.hide_password_btn.setText("")
            self._view.hide_password_icon = icons_set_color("show.svg", "#D3D3D3", icon_size)
            self._view.hide_password_btn.setIcon(self._view.hide_password_icon)
            self._view.hide_password_btn.setIconSize(icon_size)
            self._view.hide_password_btn_state = False
            logger.debug("Password is shown")

    def HotKeys(self): #Hotkeys
        hotkeys = {
            "new_password":  self.config["hotkeys"].get("new_password", "Ctrl+N"),
            "edit_password": self.config["hotkeys"].get("edit_password", "Ctrl+E"),
            "del_password": self.config["hotkeys"].get("del_password", "Ctrl+Backspace"),
            "hide_password": self.config["hotkeys"].get("hide_password", "Ctrl+G"),
            "settings": self.config["hotkeys"].get("settings", "Ctrl+I")
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

