"""
PASSWORDS-PAGE 
 Страница со всеми паролями. 
 Подгрузка данных из базы данныж и виджет просмотра конкретной карточки с информацией о пароле. 
 Обработчик клика по блоку с паролем. 
 Функция выхода из конкретного блока пароля. 
 Функция удаления конкретного пароля.
"""
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from src.setuplogger import *
from src.views.ui.icons import icons_set_color
from src.models.database.database import *


class Passwords_page(QObject):

    delete_requested = Signal(int)

    def __init__(self):
        super().__init__()

        self.password_entries = {}
        self.favorites_passwords = {}
        self.selected_password_id = None

        logger.success("Passwords page init")

        self.passwords_page()

    # Страница со всеми паролями
    def passwords_page(self):
        data = get_all_passwords()  # database get all passwords

        logger.success("all passwords cards widget init")

        # main passwords page layout 
        self.password_info_widget = QWidget()
        self.password_info_layout = QHBoxLayout(self.password_info_widget)

        # second passwords page layout 
        self.passwords_page_widget = QWidget()
        layout = QVBoxLayout(self.passwords_page_widget)

        # page title section 
        self.passwords_page_title_widget = QWidget()
        self.passwords_page_title_layout = QHBoxLayout(
            self.passwords_page_title_widget)

        # title 
        self.passwords_page_title = QLabel("All Passwords")
        self.passwords_page_title.setStyleSheet("font-size: 24pt;")

        # counter passwords
        self.passwords_count = QLabel()
        self.passwords_count.setStyleSheet("font-size: 12pt;")

        # counter favorites passwords
        self.favorites_count = QLabel("Favorites: ")
        self.favorites_count.setStyleSheet("font-size: 12pt;")

        # added widgets on layout 
        self.passwords_page_title_layout.addWidget(self.passwords_page_title)
        self.passwords_page_title_layout.addStretch()
        self.passwords_page_title_layout.addWidget(self.passwords_count)
        self.passwords_page_title_layout.addWidget(self.favorites_count)

        # connect styles for layout 
        self.passwords_page_widget.setObjectName("RightWorkspace")
        layout.setSpacing(8)

        # scroll area with passwords cards 
        self.scroll_area_all_passwords = QScrollArea()
        self.scroll_area_all_passwords.setWidgetResizable(True)
        self.scroll_area_all_passwords.setFrameShape(QFrame.Shape.NoFrame)

        # card
        self.cards_all_passwords_widget = QWidget()
        self.passwords_cards_layout = QVBoxLayout(self.cards_all_passwords_widget)
        self.passwords_cards_layout.setContentsMargins(0, 0, 0, 0)
        self.passwords_cards_layout.setSpacing(8)
        self.passwords_cards_layout.addStretch()

        # show information about current password  
        self.password_information(None, None, None, None, None, None)
        
        layout.addWidget(self.passwords_page_title_widget)
        layout.addWidget(self.passwords_page_widget)
        self.scroll_area_all_passwords.setWidget(self.cards_all_passwords_widget)
        layout.addWidget(self.scroll_area_all_passwords)
        layout.addWidget(self.main_password_information_widget)


        # hide on start menu with information about current password
        self.main_password_information_widget.hide()

        self.cards_all_passwords_widget.setStyleSheet("background-color: #111")

    def show_password_information(self, entry_id):
        """
        Функция показа информации о пароле, при клике на карточку с необходимым паролем и скрытие меню со всеми паролями. 
        Клик по карточке -> скрытие меню со всеми паролями -> показ информации о выбранном пароле.
        Кнопка back возвращает на главную страницу со всеми паролями. """
        password_data = self.password_entries.get(entry_id)

        if password_data is None:
            logger.warning(f"Password {entry_id} not found")
            return

        service, url, login, password, creation_date = password_data

        self.selected_password_id = entry_id

        # Update information
        self.title.setText(service)
        self.service_lb.setText(f"Service: {service}")
        self.url_lb.setText(f"URL: {url}")
        self.login_lb.setText(f"Login: {login}")
        self.password_lb.setText(f"Password: {password}")
        self.creation_date_lb.setText(
            f"Creation date: {creation_date}"
        )

        # Hide passwords array
        self.scroll_area_all_passwords.hide()
        self.passwords_page_title.hide()

        # Show information inside main window
        self.main_password_information_widget.show()

    def back_to_passwords(self):
        """
        Функция возвращения на главную страницу со всеми паролями. 
        Скрывает self.main_password_information_widget. Показывает тайтл и скролбар из меню со всеми паролями. Потому-что все карточки с паролями хранятся в  лайоуте скролбара.  
        """
        self.main_password_information_widget.hide()

        self.scroll_area_all_passwords.show()
        self.passwords_page_title.show()

    def delete_password_card(self, entry_id):
        # Удаляем пароль из словаря
        self.password_entries.pop(entry_id, None)

        # Находим нужную карточку
        for i in range(self.passwords_cards_layout.count()):
            item = self.passwords_cards_layout.itemAt(i)
            widget = item.widget()

            if widget is None:
                continue 

            if widget.property("entry_id") == entry_id:
                # Удаляем из layout
                self.passwords_cards_layout.removeWidget(widget)

                # Скрываем карточку
                widget.hide()

                # Уничтожаем виджет
                widget.deleteLater()

                break

        # Если удалён открытый пароль
        if self.selected_password_id == entry_id:
            self.selected_password_id = None
            self.back_to_passwords()

        logger.success(f"Password card {entry_id} removed")

    # Страница с информацией о выбранном пароле
    def password_information(self, entry_id, service, url, login, password, creation_date):

        self.main_password_information_widget = QWidget()
        self.main_password_information_layout = QHBoxLayout(
            self.main_password_information_widget)

        self.password_information_widget = QWidget()
        self.password_information_widget.setObjectName("RightWorkspace")
        self.password_info_widget.setStyleSheet("border-color: #111111")
        self.password_information_layout = QVBoxLayout(
            self.password_information_widget)

        self.title = QLabel()
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_font = self.title.font()
        label_font.setBold(True)
        self.title.setFont(label_font)
        self.title.setObjectName("RightWorkspaceTitle")

        # SERVICE
        self.service_lb = QLabel(f"Service: {service}")
        self.service_lb.setObjectName("RightWorkspaceLabel")
        self.service_lb.setTextInteractionFlags(
            Qt.TextSelectableByMouse)  # copy text

        # URL
        self.url_lb = QLabel(f"URL: {url}")
        self.url_lb.setObjectName("RightWorkspaceLabel")
        self.url_lb.setTextInteractionFlags(
            Qt.TextSelectableByMouse)  # copy text

        # LOGIN
        self.login_lb = QLabel(f"Login: {login}")
        self.login_lb.setObjectName("RightWorkspaceLabel")
        self.login_lb.setTextInteractionFlags(
            Qt.TextSelectableByMouse)  # copy text

        # PASSWORD
        self.password_lb = QLabel(f"Password: {password}")
        self.password_lb.setObjectName("RightWorkspaceLabel")
        self.password_lb.setTextInteractionFlags(Qt.TextSelectableByMouse)

        # TAG
        self.tag_lb = QLabel("Tag: ")
        self.tag_lb.setObjectName("RightWorkspaceLabel")

        # CREATION DATE
        self.creation_date_lb = QLabel(f"Creation date: {creation_date}")
        self.creation_date_lb.setObjectName("RightWorkspaceLabel")

        # DESCRIPTION
        self.description_lb = QLabel("Description:")
        self.description_lb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_lb.setObjectName("RightWorkspaceLabel")
        # TODO Описание к паролю: Добавить сохранение в базе данных
        self.description = QTextEdit()
        self.description.setObjectName("RightWorkspace")

        icon_size = QSize(24, 24)

        self.back_btn = QPushButton("")
        self.back_btn.setFixedSize(40, 40)
        self.back_btn_icon = icons_set_color(
            "arrow_left.svg", "#D3D3D3", icon_size)
        self.back_btn.setIcon(self.back_btn_icon)
        self.back_btn.setIconSize(icon_size)
        self.back_btn.setObjectName("RightWorkspaceButtons")

        self.back_btn.clicked.connect(self.back_to_passwords)

        self.hide_password_btn = QPushButton("")
        self.hide_password_btn.setFixedSize(40, 40)
        self.hide_password_btn_state = False
        self.hide_password_icon = icons_set_color(
            "show.svg", "#D3D3D3", icon_size)
        self.hide_password_btn.setIcon(self.hide_password_icon)
        self.hide_password_btn.setIconSize(icon_size)
        self.hide_password_btn.setObjectName("RightWorkspaceButtons")

        self.edit_password_btn = QPushButton("")
        self.edit_password_btn.setFixedSize(40, 40)
        self.edit_password_icon = icons_set_color(
            "edit.svg", "#D3D3D3", icon_size)
        self.edit_password_btn.setIcon(self.edit_password_icon)
        self.edit_password_btn.setIconSize(icon_size)
        self.edit_password_btn.setObjectName("RightWorkspaceButtons")

        self.delete_selected_password_btn = QPushButton("")
        self.delete_selected_password_btn.setFixedSize(40, 40)
        self.delete_selected_password_icon = icons_set_color(
            "delete.svg", "#D3D3D3", icon_size)
        self.delete_selected_password_btn.setIcon(
            self.delete_selected_password_icon)
        self.delete_selected_password_btn.setIconSize(icon_size)
        self.delete_selected_password_btn.setObjectName(
            "RightWorkspaceButtons")

        self.under_title_layout = QHBoxLayout()

        self.under_title_layout.addWidget(self.back_btn)
        self.under_title_layout.addStretch()
        self.under_title_layout.addWidget(self.hide_password_btn)
        self.under_title_layout.addWidget(self.edit_password_btn)
        self.under_title_layout.addWidget(self.delete_selected_password_btn)

        self.password_information_layout.addWidget(self.title)
        self.password_information_layout.addLayout(self.under_title_layout)
        self.password_information_layout.addWidget(self.service_lb)
        self.password_information_layout.addWidget(self.url_lb)
        self.password_information_layout.addWidget(self.login_lb)
        self.password_information_layout.addWidget(self.password_lb)
        self.password_information_layout.addWidget(self.tag_lb)
        self.password_information_layout.addWidget(self.creation_date_lb)
        self.password_information_layout.addWidget(self.description_lb)
        self.password_information_layout.addWidget(self.description)

        self.main_password_information_layout.addWidget(
            self.password_information_widget)

    # Создание секции пароля
    def all_passwords_page_add_section(self, entry_id, service_name, url, creation_date):
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
        #TODO Добавить возможность добавлять иконки к сервисам! 
        self.service_icon = ...
        self.service_name = QLabel(service_name)
        self.service_name.setStyleSheet("font-size: 18pt;")

        self.del_password_btn = QPushButton("")
        self.del_password_btn.setFixedSize(30, 30)
        self.del_password_icon = icons_set_color(
            "delete.svg", "#D3D3D3", icon_size)
        self.del_password_btn.setIcon(self.del_password_icon)
        self.del_password_btn.setIconSize(icon_size)
        self.del_password_btn.setObjectName("RightWorkspaceButtons")

        self.del_password_btn.clicked.connect(
            lambda checked=False, eid=entry_id: self.delete_requested.emit(eid))

        self.favorite_btn = QPushButton("")
        self.favorite_btn.setFixedSize(30, 30)
        self.favorite_btn_icon = icons_set_color(
            "heart.svg", "#D3D3D3", icon_size)
        self.favorite_btn.setIcon(self.favorite_btn_icon)
        self.favorite_btn.setIconSize(icon_size)
        self.favorite_btn.setObjectName("RightWorkspaceButtons")

        self.top_section_layout.addWidget(self.service_name)
        self.top_section_layout.addStretch()
        self.top_section_layout.addWidget(self.del_password_btn)
        self.top_section_layout.addWidget(self.favorite_btn)

        # bottom section widgets
        self.service_url = QLabel(url)
        self.creation_date = QLabel(creation_date)

        self.bottom_section_layout.addWidget(self.service_url)
        self.bottom_section_layout.addStretch()
        self.bottom_section_layout.addWidget(self.creation_date)

        self.section_layout.addWidget(self.top_section_widget)
        self.section_layout.addWidget(self.bottom_section_widget)

        self.section_widget.setProperty("entry_id", entry_id)

        # Делаем карточку кликабельной
        self.section_widget.setCursor(Qt.CursorShape.PointingHandCursor)
        self.section_widget.installEventFilter(self)

        # Обрабатываем нажатия на вложенные элементы
        for widget in (
            self.top_section_widget,
            self.bottom_section_widget,
            self.service_name,
            self.service_url,
            self.creation_date,
        ):
            widget.installEventFilter(self)
            widget.setCursor(Qt.CursorShape.PointingHandCursor)
            widget.setProperty("entry_id", entry_id)

        return self.section_widget

    # Обработчик кликов по карточке пароля.
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.MouseButtonRelease:
            if event.button() == Qt.MouseButton.LeftButton:
                entry_id = obj.property("entry_id")

                if entry_id is not None:
                    self.show_password_information(entry_id)
                    return True

        return super().eventFilter(obj, event)
