#main_wondow.py
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

import toml

from src.models.database.database import *
from src.setuplogger import *
from src.config_manager import ConfigManager
from src.views.ui.animations.animations import Animations

from src.views.ui.icons import icons_set_color

from src.views.ui.notifications.notifications_window import *


class MainWindow(QMainWindow):
    def __init__(self): #start
        super().__init__()

        #config
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
        logger.debug("Config successfully loaded ✅")


        
        #themes dir
        self.themes_dir = ConfigManager.get_resource_path("themes/")
        self.current_theme = f"{self.themes_dir}{self.config["view"]["theme"]}"

        self.ui()                             # load ui
        self.load_db()                        # load db
        self.apply_theme()                    # load theme

    def ui(self): #ui
        logger.debug("Main Window successfully loaded! ✅")

        self.workspace_top()   # top workspace(tool bar)
        self.workspace_left()  # left workspace
        self.workspace_right() # right workspace
        self._animations()     # animations
        self.menubar()         # menu bar
        
        # Window and startup settings
        self.setWindowTitle("CastleKeys")     # title
        self.resize(900, 700)                 # start window size
        self.setMinimumSize(900, 700)         # minimum window size

        self.central_widget = QWidget()       # Central widget
        self.workspace_container = QWidget()

        self.setCentralWidget(self.central_widget)

        self.workspace_layout = QHBoxLayout()
        main_layout = QVBoxLayout()


        self.tool_container.setLayout(self.tool_layout)

        self.workspace_layout.addWidget(self.tree_view)
        self.workspace_layout.addWidget(self.right_container)

        main_layout.addWidget(self.tool_container)
        main_layout.addLayout(self.workspace_layout)
        self.central_widget.setLayout(main_layout)
    
    def load_db(self):
        init_db()                             
        data = get_all_passwords()
        
        self.tree_model.clear()
        
        # TODO нужно писать при нажатии на корень дерева информацию о базе данных: объем базы данных, количество паролей итд. Нужно создать невидимые объекты QLabel и при нажатии на корень они стали видимыми, а если нажать на пароль, то снова невидимыми. 
        self.root_item = QStandardItem("Passwords")
        root_item_font = self.root_item.font()
        root_item_font.setBold(True)
        self.root_item.setFont(root_item_font)
        
        self.tree_model.appendRow(self.root_item)
        
        for row in data:
            self.entry_id = row[0]
            self.service_text = row[1]
            self.url_text = row[2]
            self.login_text = row[3]
            self.password_text = row[4]
            self.date_text = row[5] if len(row) > 4 else "Unknown"
            self.description_text = row[6]

            self.service_item = QStandardItem(self.service_text)

            self.service_item.setData(self.entry_id, Qt.ItemDataRole.UserRole)
            self.service_item.setData(self.login_text, Qt.ItemDataRole.UserRole + 1)
            self.service_item.setData(self.url_text, Qt.ItemDataRole.UserRole + 2)
            self.service_item.setData(self.password_text, Qt.ItemDataRole.UserRole + 3)
            self.service_item.setData(self.date_text, Qt.ItemDataRole.UserRole + 4)
            self.service_item.setData(self.description_text, Qt.ItemDataRole.UserRole + 5)

            self.root_item.appendRow(self.service_item)
            
        self.tree_view.expandAll()
        self.tree_view.isSortingEnabled()

    def apply_theme(self): #theme
        try:
            qss_styles = ConfigManager.get_main_style()
            self.setStyleSheet(qss_styles)  
            logger.debug(f"Theme {self.current_theme} successfully applied to MainWindow ✅")
        except Exception as e:
            logger.error(f"Failed to apply theme {self.current_theme}: {e}")

    def menubar(self): #menu bar
        self.menu = QMenuBar() #widget menu bar

        #file menu
        file_menu = self.menu.addMenu("File") 
        #file menu elements
        self.new_password_menu = QAction("New password", self)
        self.new_tag_menu = QAction("New tag", self)
        self.new_database_menu = QAction("New database", self)

        self.edit_password_menu = QAction("Edit menu", self)
        self.edit_database_menu = QAction("Edit database", self)

        self.import_database_menu = QAction("Import database", self)
        self.export_database_menu = QAction("Export database", self)
        self.settings_menu = QAction("Settings", self)
        #file menu add elements
        file_menu.addAction(self.new_password_menu)
        file_menu.addAction(self.new_tag_menu)
        file_menu.addAction(self.new_database_menu)
        file_menu.addSeparator()
        file_menu.addAction(self.edit_password_menu)
        file_menu.addAction(self.edit_database_menu)
        file_menu.addSeparator()
        file_menu.addAction(self.import_database_menu)
        file_menu.addAction(self.export_database_menu)
        file_menu.addSeparator()
        file_menu.addAction(self.settings_menu)

        #view menu 
        view_menu = self.menu.addMenu("View")
        #view menu elements
        change_theme = QAction("Change theme", self)
        #view menu add elemets
        view_menu.addAction(change_theme)

    def workspace_top(self): #tool_bar widgets
        logger.debug("Tool bar successfully loaded! ✅")

        self.tool_container = QWidget()
        self.tool_container.setObjectName("ToolBar")
        self.tool_layout = QHBoxLayout()

        icon_size = QSize(24, 24)
          
        self.app_title = QLabel("CastleKeys")
        self.app_title.setObjectName("ToolBarTitle")

        self.search_le = QLineEdit()
        self.search_le.setPlaceholderText("Search")
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

        self.tool_layout.addWidget(self.app_title)
        self.tool_layout.addStretch()
        self.tool_layout.addWidget(self.search_le)
        # self.tool_layout.addWidget(self.search_btn)
        self.tool_layout.addStretch()
        self.tool_layout.addWidget(self.new_password_btn)
        self.tool_layout.addWidget(self.settings_btn)

        self.settings_btn.hide()

    def workspace_left(self): #left workspace widgets
        logger.debug("Left workspace successfully loaded! ✅")

        self.left_container = QWidget()
        # self.right_container.setObjectName("RightWorkspace")
        self.left_layout = QVBoxLayout()

        self.tree_view = QTreeView()         # Tree
        self.tree_view.setObjectName("LeftWorkspace")
        self.tree_view.setAnimated(True) # opening animation
        self.tree_view.setHeaderHidden(True) # Hide header 
        self.tree_view.setFixedWidth(250)    # Width
        self.tree_view.setEditTriggers(QTreeView.EditTrigger.NoEditTriggers) # Read only
        
        self.tree_model = QStandardItemModel()

        # Привязываем созданную модель к отображению
        self.tree_view.setModel(self.tree_model)

        self.left_layout.addWidget(self.tree_view)

    def workspace_right(self): #right workspace widgets
        logger.debug("Right workspace successfully loaded! ✅")

        self.right_container = QWidget()
        self.right_container.setObjectName("RightWorkspace")
        self.right_layout = QVBoxLayout()

        self.db_information()
        self.title = QLabel()
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_font = self.title.font()
        label_font.setBold(True)
        self.title.setFont(label_font)
        self.title.setObjectName("RightWorkspaceTitle")

        # SERVICE
        self.service_lb = QLabel(f"Service: ")
        self.service_lb.setObjectName("RightWorkspaceLabel")

        #URL
        self.url_lb = QLabel("URL: ")
        self.url_lb.setObjectName("RightWorkspaceLabel")


        # LOGIN 
        self.login_lb = QLabel(f"Login: ")
        self.login_lb.setObjectName("RightWorkspaceLabel")


        # PASSWORD
        self.password_lb = QLabel(f"Password: ")
        self.password_lb.setObjectName("RightWorkspaceLabel")


        # CREATION DATE
        # NOTE Логика в том, что у пользователя может быть несколько аккаунтов одного сервиса и дата создания пароля служит ориентиром. 
        self.creation_date_lb = QLabel(f"Creation date: ")
        self.creation_date_lb.setObjectName("RightWorkspaceLabel")


        # DESCRIPTION
        self.description_lb = QLabel("Description:")
        self.description_lb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_lb.setObjectName("RightWorkspaceLabel")
        # NOTE Описание к паролю
        # Логика в том, что у пользователя может быть несколько аккаунто одного сервиса, быть аунтефикатор, чей-то аккаунт итд, описание служит ориетиром. Нужно при любом действии пользователя единожды сохранить описание.
        # Описание должно храниться в памяти компьютера при нажатии на другой пароль. При нажатии на другой пароль оно сохраняется в базу данных и при следующем заходе в программу считывает ее уже с базы данных.
        self.description = QTextEdit()
        self.description.setObjectName("RightWorkspace")



        # FIXME кнопка скрытия информации
        # Необходимо для людных мест и если рядом кто-то посторонний.
        # Логика в том, что при нажатии кнопки пароли мнгновенно скрываются, а для того, чтобы показать пароли нужно будет ввести пароль. В ИДЕАЛЕ СКРЫВАТЬ ПАРОЛИ ПОУМОЛЧАНИЮ И НЕ МЕНЯТЬ ПАРАМЕТР ВИДИМОСТИ. иконка глазика
        # Нужно сделать автоматическое скрытие при запуске программы
        # Нужно сделать поле ввода пароля при показе его снова.
        icon_size = QSize(24, 24)


        self.hide_password_btn = QPushButton("")
        self.hide_password_btn.setFixedSize(40, 40)
        self.hide_password_btn_state = False
        
        self.hide_password_icon = icons_set_color("show.svg", "#D3D3D3", icon_size)
        self.hide_password_btn.setIcon(self.hide_password_icon)
        self.hide_password_btn.setIconSize(icon_size)
        self.hide_password_btn.setObjectName("RightWorkspaceButtons")


        self.edit_password_btn = QPushButton("")
        self.edit_password_btn.setFixedSize(40, 40)
        self.edit_password_icon = icons_set_color("edit.svg", "#D3D3D3", icon_size)
        self.edit_password_btn.setIcon(self.edit_password_icon)
        self.edit_password_btn.setIconSize(icon_size)
        self.edit_password_btn.setObjectName("RightWorkspaceButtons")


        self.del_password_btn = QPushButton("")
        self.del_password_btn.setFixedSize(40, 40)
        self.del_password_icon = icons_set_color("delete.svg", "#D3D3D3", icon_size)
        self.del_password_btn.setIcon(self.del_password_icon)
        self.del_password_btn.setIconSize(icon_size)
        self.del_password_btn.setObjectName("RightWorkspaceButtons")

        self.welcome_logo = QLabel()
        self.welcome_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        welcome_logo_path = self.config["view"]["welcome_logo"]
        pixmap = QPixmap(ConfigManager.get_resource_path(welcome_logo_path))
        
        
        if not pixmap.isNull():
            # Масштабируем до 200x200 с сохранением пропорций и сглаживанием
            scaled_pixmap = pixmap.scaled(
                self.config["view"]["welcome_logo_width"], self.config["view"]["welcome_logo_height"], 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            )
            self.welcome_logo.setPixmap(scaled_pixmap)
        else:
            logger.warning("Logo image not found! Showing placeholder text.")

        self.under_title_layout = QHBoxLayout()

        right_workspace_db_information_elements = [
            self.db_size_lb,
            self.db_creation_date,
            self.path_to_db,
            self.db_count_passwords,
            self.db_count_dublicate,
            self.db_login,
            self.db_password

        ]


        self.under_title_layout.addStretch()
        self.under_title_layout.addWidget(self.hide_password_btn)
        self.under_title_layout.addWidget(self.edit_password_btn)
        self.under_title_layout.addWidget(self.del_password_btn)

        self.title.hide()
        self.welcome_logo.show()
        self.hide_password_btn.hide()
        self.edit_password_btn.hide()
        self.del_password_btn.hide()

        self.right_layout.addWidget(self.title)
        self.right_layout.addWidget(self.welcome_logo)
        self.right_layout.addLayout(self.under_title_layout)
        self.right_layout.addWidget(self.service_lb)
        self.right_layout.addWidget(self.url_lb)
        self.right_layout.addWidget(self.login_lb)
        self.right_layout.addWidget(self.password_lb)
        self.right_layout.addWidget(self.creation_date_lb)
        self.right_layout.addWidget(self.description_lb)
        self.right_layout.addWidget(self.description)

        self.title.hide()
        self.service_lb.hide()
        self.url_lb.hide()
        self.login_lb.hide()
        self.password_lb.hide()
        self.creation_date_lb.hide()
        self.description_lb.hide()
        self.description.hide()

        # Добавление элементов database_infromation
        for db_information_elements in right_workspace_db_information_elements:
            self.right_layout.addWidget(db_information_elements)
            db_information_elements.hide()

        self.right_container.setLayout(self.right_layout)

    def db_information(self): #database information widgets
        logger.debug("Database information successfully loaded! ✅")
        self.db_size_lb = QLabel()
        self.db_size_lb.setStyleSheet("font-size: 16pt; border: 0px solid #111111;")
        self.db_creation_date = QLabel()
        self.db_creation_date.setStyleSheet("font-size: 16pt; border: 0px solid #111111;")
        self.path_to_db = QLabel()
        self.path_to_db.setStyleSheet("font-size: 16pt; border: 0px solid #111111;")
        self.db_count_passwords = QLabel()
        self.db_count_passwords.setStyleSheet("font-size: 16pt; border: 0px solid #111111;")
        self.db_count_dublicate = QLabel()
        self.db_count_dublicate.setStyleSheet("font-size: 16pt; border: 0px solid #111111;")
        self.db_login = QLabel()
        self.db_login.setStyleSheet("font-size: 16pt; border: 0px solid #111111;")
        self.db_password = QLabel()
        self.db_password.setStyleSheet("font-size: 16pt; border: 0px solid #111111;")

    def _animations(self):
        #startup window opening animation 
        self.setWindowOpacity(self.config["view"]["window_opacity"])
        start_window_opening_animation = Animations.startup_window_opening_animation(
            self,
            start_value=0.0,
            end_value=self.config["view"]["window_opacity"],
            duration=self.config["view"]["window_startup_animations_duration"]
            )

        #TODO switch windows
        #Сделать анимацию при переходе между паролями, вкладками итд.
