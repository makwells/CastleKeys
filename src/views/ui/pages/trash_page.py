#trash_page.py
from PySide6.QtCore import QObject
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from src.views.ui.icons import icons_set_color

class Trash_page(QObject):
    def __init__(self):
        super().__init__()
        self.trash_page()

    def trash_page(self):
        self.trash_widget = QWidget()
        self.trash_widget.setObjectName("RightWorkspace")
        self.trash_layout = QVBoxLayout(self.trash_widget)

        title = QLabel("Trash")
        title.setStyleSheet("font-size: 24pt;")

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)


        self.trash_layout.addWidget(title)
        self.trash_layout.addWidget(scroll_area)

    def trash_cards_sections(self, entry_id, service_name, url, creation_date):
        #Full section layout
        self.trash_section_widget = QWidget()
        self.trash_section_widget.setStyleSheet("background-color: #222222; border-radius: 8px")
        self.trash_section_layout = QVBoxLayout(self.trash_section_widget)

        #Top section layout 
        self.trash_top_section_widget = QWidget()
        self.trash_top_section_layout = QHBoxLayout(self.trash_top_section_widget)
        self.trash_top_section_layout.setContentsMargins(20, 0, 0, 0)

        #Bottom section layout
        self.trash_bottom_section_widget = QWidget()
        self.trash_bottom_section_layout = QHBoxLayout(self.trash_bottom_section_widget)
        self.trash_bottom_section_layout.setContentsMargins(25, 0, 0, 0)

        icon_size = QSize(24, 24)

        #top section widgets
        service_icon = ...
        service_name = QLabel(service_name)
        service_name.setStyleSheet("font-size: 18pt;")

        self.del_password_btn = QPushButton("")
        self.del_password_btn.setFixedSize(30, 30)
        self.del_password_icon = icons_set_color("delete.svg", "#D3D3D3", icon_size)
        self.del_password_btn.setIcon(self.del_password_icon)
        self.del_password_btn.setIconSize(icon_size)
        self.del_password_btn.setObjectName("RightWorkspaceButtons")

        favorite_btn = QPushButton("")
        favorite_btn.setFixedSize(30, 30)
        favorite_btn_icon = icons_set_color("heart.svg", "#D3D3D3", icon_size)
        favorite_btn.setIcon(favorite_btn_icon)
        favorite_btn.setIconSize(icon_size)
        favorite_btn.setObjectName("RightWorkspaceButtons")

        self.trash_top_section_layout.addWidget(service_name)
        self.trash_top_section_layout.addStretch()
        self.trash_top_section_layout.addWidget(self.del_password_btn)
        self.trash_top_section_layout.addWidget(favorite_btn)

        #bottom section widgets 
        self.service_url = QLabel(url)
        self.creation_date = QLabel(creation_date)

        self.trash_bottom_section_layout.addWidget(self.service_url)
        self.trash_bottom_section_layout.addStretch()
        self.trash_bottom_section_layout.addWidget(self.creation_date)

        self.trash_section_layout.addWidget(self.trash_top_section_widget)
        self.trash_section_layout.addWidget(self.trash_bottom_section_widget)

        self.trash_section_widget.setProperty("entry_id", entry_id)

        # Делаем карточку кликабельной
        self.trash_section_widget.setCursor(Qt.CursorShape.PointingHandCursor)
        self.trash_section_widget.installEventFilter(self)

        # Обрабатываем нажатия на вложенные элементы
        for widget in (
            self.trash_top_section_widget,
            self.trash_bottom_section_widget,
            service_name,
            self.service_url,
            self.creation_date,
        ):  
            widget.installEventFilter(self)
            widget.setCursor(Qt.CursorShape.PointingHandCursor)
            widget.setProperty("entry_id", entry_id)

        return self.trash_section_widget 
    