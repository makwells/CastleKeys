#main_controller.py
from ..views.Dialogs.create_new_password import CreateNewPassword
from ..views.Dialogs.settings import Settings
from ..views.Dialogs.edit_password import Edit_Password

from ..models.db_info import Database_info

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from ..database import *
from ..setuplogger import setup_logger


class MainController():
    def __init__(self, view):
        self._view  = view      #MainWindow

        self.service_name_ = None
        self.login_ = None
        self.url_ = None
        self.password_ = None
        self.current_password = None

        self._connect_signals() #Signals

    def _connect_signals(self):
        
        self._view.tree_view.clicked.connect(self._on_category_clicked)               #tree select category
        self._view.new_password_btn.clicked.connect(self._new_password_clicked)       #new password button
        self._view.settings_btn.clicked.connect(self._setting_clicked)                #settings button
        self._view.search_btn.clicked.connect(self._search_clicked)
        self._view.edit_password_btn.clicked.connect(self._edit_password_clicked)     #edit password button 
        self._view.hide_password_btn.clicked.connect(self.hide)
        self._view.del_password_btn.clicked.connect(self._del_password_clicked)       #del password button 

        # TODO Нужно блокировать окно программы, когда открыто диалоговое окно, чтобы нельзя было открыть одновремено несколько окон добавления пароля или окон редактрирования. 

    #select category
    def _on_category_clicked(self, index):

        self.item = self._view.tree_model.itemFromIndex(index)
        item_name = self.item.text()                                  #get text
        self._view.title.setText(f"{item_name}".upper())                      #change title
        

        if self.item == self._view.root_item: # если выбран заголовок в пункте меню, то скрывать значения сервиса логина и пароля, вызвав функцию для просмотра информации о бд
            self._view.service_label.hide()
            self._view.url_lb.hide()
            self._view.login_label.hide()
            self._view.password_label.hide()
            self._view.creation_date_label.hide()
            self._view.description_label.hide()
            self._view.description.hide()
            self._view.hide_password_btn.hide()
            self._view.edit_password_btn.hide()
            self._view.del_password_btn.hide()

            self.db_information()
            return

        else: # если выбрано что-то иное то показывать
            logger.debug(f"Tree element selected: {item_name}")
            self._view.service_label.show()
            self._view.url_lb.show()
            self._view.login_label.show()
            self._view.password_label.show()
            self._view.creation_date_label.show()
            self._view.description_label.show()
            self._view.description.show()
            self._view.hide_password_btn.show()
            self._view.edit_password_btn.show()
            self._view.del_password_btn.show()

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

        self._view.service_label.setText(f"Service: {self.service_name_}")
        self._view.login_label.setText(f"Login: {self.login_}")
        self._view.url_lb.setText(f"URL: {self.url_}")
        self._view.password_label.setText(f"Password: {self.password_}")
        self._view.creation_date_label.setText(f"Creation date: {self.date_}")

        self.current_password = self._view.password_label.text()
        self.password_length = len(self.current_password)
        self.hide_password = "*" * self.password_length
            
    #add new password
    def _new_password_clicked(self):
        #open the child window to create a new password
        logger.debug("New button clicked")

        CreateNewPassword(self._view)
    
    #edit password
    def _edit_password_clicked(self):
        #open the child window to edit a password
        logger.debug("Edit button clicked")
        
        self.edit_menu = Edit_Password()
        
        get_service = self.service_name_
        get_login = self.login_
        get_password = self.password_

        # заполнять холдер текст старыми данными
        self.edit_menu.edit_input_service.setPlaceholderText(get_service)
        self.edit_menu.edit_input_login.setPlaceholderText(get_login)
        self.edit_menu.edit_input_password.setPlaceholderText(get_password)

        # TODO изменять старые данные в функции редактирования пароля

        
    def _del_password_clicked(self, tree_view):
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

    
    def _setting_clicked(self):
        #open the child window for application settings
        logger.debug("Settings button clicked")
        Settings(self._view)

    def _search_clicked(self):

        logger.debug("Search button clicked")


    def db_information(self):
        logger.debug("db_infromation clicked")
        self._view.db_size_lb.show()
        self._view.db_creation_date.show()
        self._view.path_to_db.show()
        self._view.db_count_passwords.show()
        self._view.db_count_dublicate.show()
        self._view.db_login.show()
        self._view.db_password.show()
    
    def hide(self, checked=None):
    
        if not self._view.hide_password_btn_state:
            self._view.password_label.setText("Password: " + self.hide_password) 
            self._view.hide_password_btn.setText("Show")
            self._view.hide_password_btn_state = True
            logger.debug("Password hidden")
        else:
            self._view.password_label.setText(self.current_password)
            self._view.hide_password_btn.setText("Hide")
            self._view.hide_password_btn_state = False
            logger.debug("Password is shown")
