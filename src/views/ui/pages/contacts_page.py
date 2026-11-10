#contacts_page.py 

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from src.setuplogger import *
from src.views.ui.icons import icons_set_color


class Contacts_page(QObject):
    def __init__(self):
        super().__init__()

        logger.success("Contacts page init")
        self.contacts_page()

    def contacts_page(self):
        logger.debug("all contacts cards widget init")

        self.contacts_widget = QWidget()
        self.contacts_layout = QVBoxLayout(self.contacts_widget)

        title = QLabel("Contacts")
        title.setStyleSheet("font-size: 24pt;")


        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        self.contacts_layout.addWidget(title)
        self.contacts_layout.addWidget(scroll_area)
        self.contacts_widget.setObjectName("RightWorkspace")

        self.cards_all_contacts_widget = QWidget()
        self.contacts_cards_layout = QVBoxLayout(self.cards_all_contacts_widget)
        self.contacts_cards_layout.addStretch()
        self.contacts_cards_layout.setContentsMargins(0, 0, 0, 0)
        self.contacts_cards_layout.setSpacing(8)

        scroll_area.setWidget(self.cards_all_contacts_widget)

        self.contact_card(
            first_name="Ivan",
            last_name="Ivanov",
            surname="Ivanovich",
            phone_number="89160000000",
            social="true",
            description="Ivan, made in china ",
            country="🇷🇺"
            )

        self.contacts_cards_layout.addWidget(self.section_widget)

        self.cards_all_contacts_widget.setStyleSheet("background-color: #111")

        
        #TODO Метод, который будет создавать карточку контакта, по принципу с созданием пароля. Привязать все кнопки в класс main_controller.py. Хранить все контакты в отдельной от паролей базе данных.  

    
    def contact_card(
            self,
            first_name,     # Имя
            last_name,      # Фамилия 
            surname,        # Отчество
            phone_number,   # Основной номер телефона
            social,         # Социальные сети
            description,    # Комментарий
            country
            ):
        # Full section layout
        self.section_widget = QWidget()
        self.section_widget.setStyleSheet(
            "background-color: #222222; border-radius: 8px")
        self.section_layout = QVBoxLayout(self.section_widget)

        # Top section layout
        self.top_section_widget = QWidget()
        self.top_section_layout = QHBoxLayout(self.top_section_widget)
        self.top_section_layout.setContentsMargins(20, 0, 0, 0)

        # Bottom section layout
        self.bottom_section_widget = QWidget()
        self.bottom_section_layout = QHBoxLayout(self.bottom_section_widget)
        self.bottom_section_layout.setContentsMargins(25, 0, 0, 0)

        icon_size = QSize(24, 24)

        # top section widgets
        # name 
        self.contact_name = QLabel(f"{last_name} {first_name} {surname}") 
        
        self.contact_name.setStyleSheet("font-size: 18pt;")

        # phone number 
        self.phone_number = QLabel(f"{phone_number}")

        #del button 
        self.del_password_btn = QPushButton("")
        self.del_password_btn.setFixedSize(30, 30)
        self.del_password_icon = icons_set_color(
            "delete.svg", "#D3D3D3", icon_size)
        self.del_password_btn.setIcon(self.del_password_icon)
        self.del_password_btn.setIconSize(icon_size)
        self.del_password_btn.setObjectName("RightWorkspaceButtons")

        #favorite button 
        self.favorite_btn = QPushButton("")
        self.favorite_btn.setFixedSize(30, 30)
        self.favorite_btn_icon = icons_set_color(
            "heart.svg", "#D3D3D3", icon_size)
        self.favorite_btn.setIcon(self.favorite_btn_icon)
        self.favorite_btn.setIconSize(icon_size)
        self.favorite_btn.setObjectName("RightWorkspaceButtons")

        self.top_section_layout.addWidget(self.contact_name)
        self.top_section_layout.addStretch()
        self.top_section_layout.addWidget(self.phone_number)
        self.top_section_layout.addWidget(self.del_password_btn)
        self.top_section_layout.addWidget(self.favorite_btn)

        # bottom section widgets
        self.description = QLabel(description)
        self.country = QLabel(country)

        self.bottom_section_layout.addWidget(self.description)
        self.bottom_section_layout.addStretch()
        self.bottom_section_layout.addWidget(self.country)

        self.section_layout.addWidget(self.top_section_widget)
        self.section_layout.addWidget(self.bottom_section_widget)

        # self.section_widget.setProperty("entry_id", entry_id)

        # Делаем карточку кликабельной
        self.section_widget.setCursor(Qt.CursorShape.PointingHandCursor)
        self.section_widget.installEventFilter(self)

        # Обрабатываем нажатия на вложенные элементы
        for widget in (
            self.top_section_widget,
            self.bottom_section_widget,
            self.contact_name,
            self.phone_number,
            self.description,
        ):
            widget.installEventFilter(self)
            widget.setCursor(Qt.CursorShape.PointingHandCursor)
            # widget.setProperty("entry_id", entry_id)

        return self.section_widget


    # Обработчик кликов по карточке пароля.
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.MouseButtonRelease:
            if event.button() == Qt.MouseButton.LeftButton:
                entry_id = obj.property("entry_id")

                if entry_id is not None:
                    # self.show_password_information(entry_id)
                    return True

        return super().eventFilter(obj, event)