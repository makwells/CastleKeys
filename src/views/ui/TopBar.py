#TopBar.py
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from src.setuplogger import *
from src.config_manager import ConfigManager

from src.models.database.database import *

from src.views.ui.animations.animations import Animations
from src.views.ui.icons import icons_set_color
from src.views.ui.notifications.notifications_window import *

from pathlib import Path


class TopBar:
    def __init__(self):
        self.init_topbar()

    def init_topbar(self):
            # def workspace_top(self): #tool_bar widgets
        logger.debug("Tool bar successfully loaded! ✅")

        self.tool_container = QWidget()
        self.tool_container.setObjectName("ToolBar")
        self.tool_layout = QHBoxLayout(self.tool_container)

        icon_size = QSize(24, 24)
          
        self.app_title = QLabel("CastleKeys")
        self.app_title.setObjectName("ToolBarTitle")

        self.search_le = QLineEdit()
        self.search_le.setPlaceholderText("Search passwords...")
        self.search_le.setFixedSize(500, 30)
        self.search_le.setObjectName("ToolBarSearch")

        self.new_password_btn = QPushButton("")
        self.new_password_btn.setFixedSize(40, 30)
        self.new_password_icon = icons_set_color("add.svg", "#D3D3D3", icon_size)
        self.new_password_btn.setIcon(self.new_password_icon)
        self.new_password_btn.setIconSize(icon_size)
        self.new_password_btn.setObjectName("ToolBarButtons")

        self.settings_btn = QPushButton()
        self.settings_btn.setFixedSize(40, 30)
        self.settings_icon = icons_set_color("settings.svg", "#D3D3D3", icon_size)
        self.settings_btn.setIcon(self.settings_icon)
        self.settings_btn.setIconSize(icon_size)
        self.settings_btn.setObjectName("ToolBarButtons")

        self.tool_layout.addStretch()
        self.tool_layout.addWidget(self.app_title)
        self.tool_layout.addStretch()
        self.tool_layout.addWidget(self.search_le)
        # self.tool_layout.addWidget(self.search_btn)
        # self.tool_layout.addStretch()
        self.tool_layout.addWidget(self.new_password_btn)
        self.tool_layout.addWidget(self.settings_btn)

        # self.settings_btn.hide()

