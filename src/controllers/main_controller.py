#main_controller.py
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from src.views.Dialogs.create_new_password import CreateNewPassword
from src.views import Settings
from src.views import Edit_Password
from src.views import icons_set_color

from src.models.database import database
from src.models import Database_info
from src.models import hotkeys

from src.setuplogger import *
from src import ConfigManager

from . import search

from datetime import datetime




# FIXME Изменить логику редактирования пароля. Нужно сделать редактирование в реальном времени, также как и создание нового пароля.
# FIXME если пароль изменить, а после пару раз скрыть и открыть пароль, то пароль в интерфейсе заменяется на пустое значение, при этом он меняется только в интерфейсе, в базе данных он не изменяется. Дело в функции редактирования пароля или в скрытии.

# TODO Добавление стилей для диалоговых окон. 
# TODO Создать подтверждения пароля от базы данных.  
# TODO добавить окно с информацией о бд. Чтобы зайти в это окно, нужно будет ввести логин и пароль от базы данных. Там же их можно будет и поменять. 
# TODO Сделать уведомления, которые будут всплывать, когда пользователь будет взаимодействовать с программой: "Пароль успешно создан", "Пароль успешно удален". Но эти уведомления должны быть всплывающими в интерфейсе самой программы, а не системно. Перекрывая часть интерфейса(пример vscode). Добавить возможность менять углы(левый верхний, правый нижний итд)
# TODO Сделать поиск
# TODO Сделать настройки

class MainController():
    def __init__(self, view):

        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()

        self._view = view #MainWindow
        self.search_field = search.Search(self._view)

        self.search_field.search_text.connect(self.find_password)

        self.service_name_ = None
        self.login_ = None
        self.url_ = None
        self.password_ = None
        self.current_password = None

        self._connect_signals() #Connects


    # connect signals
    def _connect_signals(self):
        
        self._view.tree_view.clicked.connect(self._on_category_clicked)               #tree select category
        self._view.new_password_btn.clicked.connect(self._new_password_clicked)       #new password menu(button)
        self._view.settings_btn.clicked.connect(self._setting_clicked)                #settings menu(button)
        self._view.edit_password_btn.clicked.connect(self._edit_password_clicked)     #edit password menu(button)
        self._view.hide_password_btn.clicked.connect(self.hide)                       #hide password(button)
        self._view.del_password_btn.clicked.connect(self._del_password_clicked)       #del password(button)

        self._view.new_password_menu.triggered.connect(self._new_password_clicked)    #new password menu(menubar)
        self._view.edit_password_menu.triggered.connect(self._edit_password_clicked)  #edit password(menu)
        self._view.settings_menu.triggered.connect(self._setting_clicked)             #settings menu(menu)

        # self._view.search_le.textChanged.connect(self._search)

        hotkeys.HotKeys(self)      # Connect hotkeys


    # select category
    def _on_category_clicked(self, index): 
        real_index = self._view.proxy_model.mapToSource(index)
        self.item = self._view.tree_model.itemFromIndex(real_index) #current element
        item_name = self.item.text()                           #get text
        self._view.title.setText(f"{item_name}".upper())       #change title
        

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
            self._view.welcome_logo.hide()

            self._view.edit_password_menu.blockSignals(True)

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

            #unblock signals
            self._view.edit_password_menu.blockSignals(False)
            self._view.del_password_btn.setEnabled(True)

            # self._view.service_item.setSelectable(True)

            if self.config["privacy"]["auto_hide_passwords"]:
                self._view.hide_password_btn_state = False
            

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

        #auto hide passwords
        if self.config["privacy"]["auto_hide_passwords"]:
            self.hide()
        else:
            return

    # add new password
    def _new_password_clicked(self):
        logger.success("Run new password window form")

        #FIXME если написать сервис, а потом стереть его и отменить, то последний символ все равно сохранится.

        self.new_window = CreateNewPassword(self._view)

        self._new_password_saved = False 
        self._new_tree_item = None
        self._current_new_id = None

        self.new_window.data_created_password.connect(self._update_ui_new_password_realtime)
        self.new_window.exec()

    # add new password realtime update ui
    def _update_ui_new_password_realtime(self, data: dict):
        get_service = data.get("service", "")
        get_url = data.get("url", "")
        get_login = data.get("login", "")
        get_password = data.get("password", "")

        if not self._new_password_saved:
            new_id = database.add_password(
                service=get_service,
                url=get_url,
                login=get_login,
                password=get_password
            )

            if new_id and new_id != -1:
                self._new_password_saved = True
                self._current_new_id = new_id
                
                current_date = datetime.now().strftime("%Y-%m-%d %H:%M") # get current date
                # Create element on tree
                service_item = QStandardItem(get_service or "New Entry")
                service_item.setData(self._current_new_id, Qt.ItemDataRole.UserRole) # current id
                service_item.setData(get_login, Qt.ItemDataRole.UserRole + 1)    # current login
                service_item.setData(get_url, Qt.ItemDataRole.UserRole + 2)      # current url 
                service_item.setData(get_password, Qt.ItemDataRole.UserRole + 3) # current password
                service_item.setData(current_date, Qt.ItemDataRole.UserRole + 4) # current date 
                service_item.setData("", Qt.ItemDataRole.UserRole + 5)           

                self._view.root_item.appendRow(service_item)
                self._new_tree_item = service_item
                logger.debug(f"New password created in DB with ID {self._current_new_id}")

        elif self._new_password_saved and self._current_new_id is not None:
            success = database.update_password(
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

    # edit password
    def _edit_password_clicked(self):
        logger.debug("Run edit password window form")
        
        self.edit_window = Edit_Password()
        
        get_service = self.service_name_
        get_url = self.url_
        get_login = self.login_
        get_password = self.password_

        # fild holdertext old data
        self.edit_window.edit_input_service.setPlaceholderText(get_service)
        self.edit_window.edit_input_login.setPlaceholderText(get_login)
        self.edit_window.edit_input_url.setPlaceholderText(get_url)
        self.edit_window.edit_input_password.setPlaceholderText(get_password)

        # get signal
        self.edit_window.data_edit_password.connect(self._update_ui_edited)

        self.edit_window.exec() # execute edit window

    # update edited passwords
    def _update_ui_edited(self, data:dict):
        #get edited password 
        new_service  = data.get("service") or self.service_name_
        new_url      = data.get("url") or self.url_
        new_login    = data.get("login") or self.login_
        new_password = data.get("password") or self.password_
        
        if new_service != "": logger.debug(f"Received updated service data: {new_service}") # if service = Null return old data
        if new_url != "": logger.debug(f"Received updated url data: {new_url}") # if url = Null return old data
        if new_login != "": logger.debug(f"Received updated login data: {new_login}") # if login = Null return old data
        if new_password != "": logger.debug(f"Received updated password data: {new_password}")# if password = Null return old data

        # change in db
        success = database.update_password(
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

            self.item.setText(self.service_name_)                     # title on tree 
            self._view.title.setText(f"{self.service_name_}".upper()) # title on right_workspace

    # delete password
    def _del_password_clicked(self, tree_view): 
        logger.debug("Run delete confirmation window")

        reply = QMessageBox.question(
            None, 
            "Confirmation", 
            "Are you sure you want to delete the password?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            logger.success("Password deleted.")
            #Get current index element
            current_index = self._view.tree_view.currentIndex()
    
            if not current_index.isValid():
                return
    
            model = self._view.tree_view.model() 
            row = current_index.row()
            parent_index = current_index.parent()
    
            # index first row
            first_column_index = model.index(row, 0, parent_index)
            
            #get database id 
            db_id = model.data(first_column_index, Qt.ItemDataRole.UserRole)
    
            if db_id is None:
                logger.error("The database identifier is missing from the interface element!")
                return
    
            #delete
            if database.delete_password(db_id):
                model.removeRow(row, parent_index)
                logger.success(f"The row with ID {db_id} has been removed from the interface.")

            self.main_menu()
        else:
            logger.debug("Deletion cancelled.")
            return      

    # settings
    def _setting_clicked(self): 
        #open the child window for application settings
        logger.debug("Run settings menu")
        Settings(self._view).exec()

    # seach
    def find_password(self, data: dict):
        search_text = data.get("text", "")

        self._view.proxy_model.setRecursiveFilteringEnabled(True)
        self._view.proxy_model.setFilterKeyColumn(0)  # Filter by service name
        self._view.proxy_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

        # We pass the text to the proxy models. 
        self._view.proxy_model.setFilterFixedString(search_text)



    # database information
    def db_information(self):
        logger.debug("Run database info window")
        self._view.db_size_lb.show()
        self._view.db_creation_date.show()
        self._view.path_to_db.show()
        self._view.db_count_passwords.show()
        self._view.db_count_dublicate.show()
        self._view.db_login.show()
        self._view.db_password.show()
        
        self._view.db_size_lb.setText(f"Database size: {Database_info.db_size(self, "Passwords/passwords.db")}") #database size

    # hide/show passwords
    def hide(self, checked=None): 
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

    def main_menu(self):
        logger.debug("Run main menu")
        
        # hide all elements right workspace
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
        self._view.db_size_lb.hide()
        self._view.db_creation_date.hide()
        self._view.path_to_db.hide()
        self._view.db_count_passwords.hide()
        self._view.db_count_dublicate.hide()
        self._view.db_login.hide()
        self._view.db_password.hide()

        # show logo
        self._view.welcome_logo.show()

