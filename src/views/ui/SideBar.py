#SideBar.py
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from src.setuplogger import *

from src.views.ui.icons import icons_set_color

class SideBar(QObject): 
    def __init__(self, pages):
        super().__init__() 

        logger.success("Sidebar init")
        self.init_sidebar()

        self.pages = pages

    def init_sidebar(self):
        self.sidebar_widget = QWidget()
        self.sidebar_widget.setObjectName("LeftWorkspace")
        self.sidebar_widget.setFixedWidth(250)

        self.sidebar_layout = QVBoxLayout(self.sidebar_widget)

        #Buttons 
        self.all_passwords_btn = QPushButton("All passwords")
        self.favorites_btn = QPushButton("Favorite passwords")
        self.contacts_btn = QPushButton("Contacts")
        self.cards_btn = QPushButton("Cards")
        self.tokens_btn = QPushButton("Tokens")
        self.wifi_btn = QPushButton("Wi-Fi")
        self.trash_btn = QPushButton("Trash")


        #Добавление кнопок в интерфейс 
        self.sidebar_layout.addWidget(self.all_passwords_btn)
        self.sidebar_layout.addWidget(self.favorites_btn)
        self.sidebar_layout.addWidget(self.contacts_btn)
        self.sidebar_layout.addWidget(self.cards_btn)
        self.sidebar_layout.addWidget(self.tokens_btn)
        self.sidebar_layout.addWidget(self.wifi_btn)
        self.sidebar_layout.addStretch()
        self.sidebar_layout.addWidget(self.trash_btn)


        #Подключение действий к кнопкам в sidebar
        #Passwords Page
        self.all_passwords_btn.clicked.connect(
            lambda: self.pages.setCurrentWidget(self.pages.passwords_page.passwords_page_widget))

        #Favorites Page
        self.favorites_btn.clicked.connect(
            lambda: self.pages.setCurrentWidget(self.pages.favorites_page.favorites_widget))
        
        #Contact Page
        self.contacts_btn.clicked.connect(
            lambda: self.pages.setCurrentWidget(self.pages.contacts_page.contacts_widget)
            )

        #Cards Page
        self.cards_btn.clicked.connect(
            lambda: self.pages.setCurrentWidget(self.pages.cards_page.cards_widget)
            )

        #Tokens Page
        self.tokens_btn.clicked.connect(
            lambda: self.pages.setCurrentWidget(self.pages.tokens_page.tokens_widget)
        )

        #WiFi Page
        self.wifi_btn.clicked.connect(
            lambda: self.pages.setCurrentWidget(self.pages.wifi_page.wifi_widget)
        )

        #Trash Page
        self.trash_btn.clicked.connect(
            lambda: self.pages.setCurrentWidget(self.pages.trash_page.trash_widget)
        )