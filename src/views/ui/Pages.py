"""
PAGES 
Главный класс, работы со страницами. 
Переключение между страницами и подключение базы данных.
Доступные страницы:
    * Passwords
    * Favorites 
    * Contacts 
    * Cards
    * Tokens
    * Wi-Fi
    * Trash
"""

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from src.setuplogger import *

from src.models.database.database import *
from src.views.ui.notifications.notifications_window import *

from src.views.ui.pages.mainMenu_page import Main_menu_page
from src.views.ui.pages.passwords_page import Passwords_page
from src.views.ui.pages.contacts_page import Contacts_page 
from src.views.ui.pages.favorites_page import Favorites_page
from src.views.ui.pages.cards_page import Cards_page
from src.views.ui.pages.tokens_page import Tokens_page
from src.views.ui.pages.wifi_page import WiFi_page
from src.views.ui.pages.trash_page import Trash_page

class Pages(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.main_menu_page = Main_menu_page()
        self.passwords_page = Passwords_page()
        self.favorites_page = Favorites_page()
        self.contacts_page = Contacts_page()  
        self.cards_page = Cards_page()
        self.tokens_page = Tokens_page()
        self.wifi_page = WiFi_page()
        self.trash_page = Trash_page()

        self.password_entries = {}
        self.selected_password_id = None

        logger.success("Pages init.")

        self.load_pages()
        self.load_db()


    def load_pages(self):
        #Add main menu page
        self.addWidget(self.main_menu_page.main_menu_widget)
        logger.success("Passwords page init.")

        #Add passwords page
        self.addWidget(self.passwords_page.passwords_page_widget)
        logger.success("Passwords page init.")

        #Add favorites page
        self.addWidget(self.favorites_page.favorites_widget)
        logger.success("Favorites page init.")

        #Add contacts page
        self.addWidget(self.contacts_page.contacts_widget)
        logger.success("Contacts page init.")

        #Add cards page
        self.addWidget(self.cards_page.cards_widget)
        logger.success("Cards page init.")

        #Add tokens page 
        self.addWidget(self.tokens_page.tokens_widget)
        logger.success("Tokens page init.")

        #Add Wi-Fi page
        self.addWidget(self.wifi_page.wifi_widget)
        logger.success("WiFi page init.")

        #Add trash page
        self.addWidget(self.trash_page.trash_widget)
        logger.success("Trash page init.")


    def load_db(self):
        # try:
        init_db() #init database
        data = get_all_passwords() #database get all passwords
        self.count_passwords = len(data)
        self.count_favorites = None
        self.passwords_page.passwords_count.setText(f"Count: {self.count_passwords}")
        self.passwords_page.favorites_count.setText(f"Favorites: {self.count_favorites}")

        # Очищаем старые карточки
        while self.passwords_page.passwords_cards_layout.count():
            layout_item = self.passwords_page.passwords_cards_layout.takeAt(0)
            widget = layout_item.widget()

            if widget is not None:
                widget.hide()
                widget.deleteLater()

        self.passwords_page.password_entries.clear()

        for row in data:
            entry_id = row[0]
            service_name = row[1]
            url = row[2]
            login = row[3]
            password = row[4]
            creation_date = row[5] if len(row) > 5 else "Unknown"

            self.passwords_page.password_entries[entry_id] = (
                service_name,
                url,
                login,
                password,
                creation_date
            )

            password_card = self.passwords_page.all_passwords_page_add_section(
                entry_id=entry_id,
                service_name=service_name,
                url=url,
                creation_date=creation_date
            )

            self.passwords_page.passwords_cards_layout.addWidget(password_card)

        self.passwords_page.passwords_cards_layout.addStretch()
