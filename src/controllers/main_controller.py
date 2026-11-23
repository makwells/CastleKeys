#main_controller.py
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from src.views import CreateNewPassword
from src.views import Password_Confirmation
from src.views import Settings
from src.views import Edit_Password
from src.views import icons_set_color

from src.models.database import database
from src.models import Database_info
from src.models import hotkeys

from src.setuplogger import *
from src import ConfigManager

from src.controllers.search import Search

from datetime import datetime

class MainController():
    def __init__(self, view, pages, topbar):

        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()

        self._view = view                           #MainWindow
        self._pages = pages                         #Pages
        self._topbar = topbar                       #Topbar
        self.search_field = Search(self._view)      #Search 

        self.service_name_ = None
        self.login_ = None
        self.url_ = None
        self.password_ = None

        self._connect_signals() #Connects
        hotkeys.HotKeys(self)   # Connect hotkeys


    # connect signals
    def _connect_signals(self):
        #search 
        self.search_field.search_text.connect(self.find_password) 
        #settings menu(button)
        self._view.topbar.settings_btn.clicked.connect(self._setting_clicked)
        #edit password menu(button)
        self._pages.passwords_page.edit_password_btn.clicked.connect(self._edit_password_clicked)     
        #hide password
        self._pages.passwords_page.hide_password_btn.clicked.connect(self.hide)                       

        """
        Объяснение: Если открыта страница с паролями, то кнопка Add будет адресована только странице с паролями. Добавить пароль с вкладки контактов невозможно. 
        Если открыта страница с контактами, то кнопка Add будет адресованна только странице с контактами. Добавить контакт с вкладки паролей невозможно. 

        Проще говоря, для каждой вкладки - свой функционал кнопки Add
        """
        self._view.topbar.new_password_btn.clicked.connect(self._add_entry_clicked)
        self._pages.currentChanged.connect(self._update_add_button)
        self._update_add_button()


        self._pages.passwords_page.delete_requested.connect(self._del_password_clicked)
        self._pages.passwords_page.delete_selected_password_btn.clicked.connect(lambda checked=False: self._del_password_clicked())
    
    # Включает кнопку только на странице паролей
    def _update_add_button(self, index=None):
        is_passwords_page = (
            self._pages.currentWidget()
            is self._pages.passwords_page.passwords_page_widget
        )
        self._view.topbar.new_password_btn.setEnabled(is_passwords_page)

    # Проверяет текущую страницу и открывает окно создания пароля.
    def _add_entry_clicked(self, checked=False):
        if (
            self._pages.currentWidget()
            is self._pages.passwords_page.passwords_page_widget
        ):
            self._new_password_clicked()

    def favorites_func(self):
        logger.debug("Favorite")

        icon_size = QSize(24, 24)
        self._pages.passwords_page.favorite_btn_icon = icons_set_color("heart_filled.svg", "#D3D3D3", icon_size)
        self._pages.passwords_page.favorite_btn.setIcon(self._pages.passwords_page.favorite_btn_icon)
        self._pages.passwords_page.favorite_btn.setIconSize(icon_size)
        

    # add new password
    #FIXME: После добавления пароля его нельзя открыть. Открывается он лишь после перезапуска всего приложения. 
    def _new_password_clicked(self):
        logger.success("Run new password window form")

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
         
                self.card = self._pages.passwords_page.all_passwords_page_add_section(
                    entry_id = self._current_new_id,
                    service_name=get_service or "new Entry",
                    url=get_url or "Unknow",
                    creation_date=current_date or "Unknow",
                )

                cards_layout = self._pages.passwords_page.passwords_cards_layout
                # Вставляем карточку перед растяжкой в конце списка.
                cards_layout.insertWidget(
                    max(0, cards_layout.count() - 1),
                    self.card,
                )

                logger.debug(f"New password created in DB with ID {self._current_new_id}")

        elif self._new_password_saved and self._current_new_id is not None:
            success = database.update_password(
                password_id=self._current_new_id,
                service=get_service,
                url=get_url,
                login=get_login,
                password=get_password
            )

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
        
        if new_service != "": logger.debug("Received updated service data") # if service = Null return old data
        if new_url != "": logger.debug("Received updated url data") # if url = Null return old data
        if new_login != "": logger.debug("Received updated login data") # if login = Null return old data
        if new_password != "": logger.debug("Received updated password data")# if password = Null return old data

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
            self._pages.passwords_page.service_lb.setText(f"Service: {new_service}") 
            self._pages.passwords_page.url_lb.setText(f"URL: {new_url}")
            self._pages.passwords_page.login_lb.setText(f"Login: {new_login}")
            self._pages.passwords_page.password_lb.setText(f"Password: {new_password}")

            self.service_name_ = new_service
            self.url_ = new_url
            self.login_ = new_login
            self.password_ = new_password

            # self.item.setText(self.service_name_)                     # title on tree 
            self._pages.passwords_page.title.setText(f"{self.service_name_}".upper()) # title on right_workspace

    # delete password
    #FIXME: Подтверждение: Переделать диалоговое окно подтверждения удаления пароля под стилистику программы.
    #FIXME: После добавления пароля его нельзя удалить. Удаляется он лишь после перезапуска всего приложения.
    #TODO: переделать логику удаления: после нажатия кнопки удаления на пароле он переноситься на страницу "trash", после чего его можно будет удалить окончательно из базы данных. 
    #TODO: На данный момент больше всего сделана страница с паролями: блокировать поиск, если страница с паролями не выбрана. 

    def _del_password_clicked(self, entry_id=None):
        page = self._pages.passwords_page

        if entry_id is None:
            entry_id = page.selected_password_id

        if entry_id is None:
            logger.warning("Password is not selected.")
            return

        reply = QMessageBox.question(
            self._view,
            "Confirmation",
            "Are you sure you want to delete the password?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply != QMessageBox.StandardButton.Yes:
            logger.debug("Deletion cancelled.")
            return

        if not database.delete_password(entry_id):
            logger.error(f"Failed to delete password {entry_id}.")
            QMessageBox.warning(
                self._view,
                "Error",
                "Failed to delete password.",
            )
            return

        page.delete_password_card(entry_id)   
        logger.success(f"Password {entry_id} deleted.")

    # settings
    def _setting_clicked(self): 
        #open the child window for application settings
        logger.debug("Run settings menu")
        Settings(self._view).exec() 

    # Search
    #FIXME: Сделать поиск даже на главной странице. При вводе текста искать совпадения во всех страницах и выводить отдельной страницей(Find Page). 
    def find_password(self, data: dict):
        query = data.get("text", "").strip().casefold()
        layout = self._pages.passwords_page.passwords_cards_layout

        for index in range(layout.count()):
            card = layout.itemAt(index).widget()

            if card is None:
                continue

            # В текущей структуре карточки первый QLabel — название сервиса.
            service_label = card.findChild(QLabel)
            service = (
                service_label.text().casefold()
                if service_label is not None
                else ""
            )

            card.setVisible(not query or query in service)

    # database information
    #TODO: Информация о базе данных: Переделать под новый интерфейс программы. Перенести во вкладку настроек.
    def db_information(self):
        logger.debug("Run database info window")
        self._view.db_size_lb.show()
        self._view.db_creation_date.show()
        self._view.path_to_db.show()
        self._view.db_count_passwords.show()
        self._view.db_count_dublicate.show()
        self._view.db_login.show()
        self._view.db_password.show()

        get_database_path = self.config_manager.database_get_path()
        
        self._view.db_size_lb.setText(f"Database size: {Database_info.db_size(self, f"{get_database_path}")}") #database size
        self._view.path_to_db.setText(f"Database path: {get_database_path}") #database path
        self._view.db_count_passwords.setText(f"Database count passwords: {database.get_count_passwords()}") #database count passwords

    # hide/show passwords
    def hide(self, checked=None):
        #FIXME: сркытие пароля: пароль скрывается, но обратно не показывается, звездочки добавляются снова и снова до бесконечности. Нужно вызывать раньше, чем метод скрытия. 
        #FIXME: автоматическое скрытие пароля: скрывать пароли при запуске программы и переключении между ними. 
        #FIXME: показ пароля: перед тем, как показать пароль нужно сначала его подтвердить. Добавить параметр для отключение подтверждения. 
        self.current_password = self._pages.passwords_page.password_lb.text()
        self.password_length = len(self.current_password)
        self.hide_password = "*" * self.password_length 

        icon_size = QSize(24, 24)

        if not self._pages.passwords_page.hide_password_btn_state:
            self._pages.passwords_page.password_lb.setText("Password: " + self.hide_password) 
            self._pages.passwords_page.hide_password_btn.setText("")
            self._pages.passwords_page.hide_password_icon = icons_set_color("hide.svg", "#D3D3D3", icon_size)
            self._pages.passwords_page.hide_password_btn.setIcon(self._pages.passwords_page.hide_password_icon)
            self._pages.passwords_page.hide_password_btn.setIconSize(icon_size)

            self._pages.passwords_page.hide_password_btn_state = True
            logger.debug("Password hidden")
        else:

            self._pages.passwords_page.password_lb.setText(self.current_password)
            self._pages.passwords_page.hide_password_btn.setText("")
            self._pages.passwords_page.hide_password_icon = icons_set_color("show.svg", "#D3D3D3", icon_size)
            self._pages.passwords_page.hide_password_btn.setIcon(self._pages.passwords_page.hide_password_icon)
            self._pages.passwords_page.hide_password_btn.setIconSize(icon_size)
            self._pages.passwords_page.hide_password_btn_state = False
            logger.debug("Password is shown")

    def main_menu(self):
        logger.debug("Run main menu")
        self._pages.setCurrentIndex(0)
