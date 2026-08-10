#main_wondow.py
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

import toml

from ..database import *
from ..setuplogger import setup_logger
from .icons import icons_set_color
from .theme_manager import ConfigManager

class MainWindow(QMainWindow):
    def __init__(self): #start
        super().__init__()

        # Config
        with open("config.toml", "r", encoding="utf-8") as config_file:
            logger.success("Config successfully loaded ✅")
            self.config = toml.load(config_file)


        self.themes_dir = "themes/"
        self.current_theme = f"{self.themes_dir}{self.config["view"]["theme"]}"

        self.apply_theme()                    # load theme
        self.init_ui()                        # load ui
        self.load_db()                        # load db

    def apply_theme(self): #init theme
        try:
            style = ConfigManager.get_style()
            self.setStyleSheet(style)
            logger.success(f"Theme {self.current_theme} successfully applied to MainWindow ✅")
        except Exception as e:
            logger.error(f"Failed to apply theme {self.current_theme}: {e}")

    def init_ui(self): #init ui
        logger.debug("Main Window successfully loaded! ✅")

        self.tool_bar()                       # Tool bar
        self.workspace_l()                    # Left workspace
        self.workspace_r()                    # Right workspace
        self.animations()
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
    
    def load_db(self): #init database
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

            service_item = QStandardItem(self.service_text)

            service_item.setData(self.entry_id, Qt.ItemDataRole.UserRole)
            service_item.setData(self.login_text, Qt.ItemDataRole.UserRole + 1)
            service_item.setData(self.url_text, Qt.ItemDataRole.UserRole + 2)
            service_item.setData(self.password_text, Qt.ItemDataRole.UserRole + 3)
            service_item.setData(self.date_text, Qt.ItemDataRole.UserRole + 4)
            service_item.setData(self.description_text, Qt.ItemDataRole.UserRole + 5)

            self.root_item.appendRow(service_item)
            
        self.tree_view.expandAll()

    def tool_bar(self): #tool_bar widgets
        logger.debug("Tool bar successfully loaded! ✅")

        self.tool_container = QWidget()
        self.tool_container.setObjectName("ToolBar")
        self.tool_layout = QHBoxLayout()

        icon_size = QSize(24, 24)
          
        self.app_title = QLabel("CastleKeys")
        self.app_title.setObjectName("ToolBarTitle")

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search")
        self.search.setFixedSize(500, 30)
        self.search.setObjectName("ToolBarSearch")

        self.search_btn = QPushButton()
        self.search_btn.setFixedSize(40, 30)
        self.search_icon = icons_set_color("search.svg", "#D3D3D3", icon_size)
        self.search_btn.setIcon(self.search_icon)
        self.search_btn.setIconSize(icon_size)
        self.search_btn.setObjectName("ToolBarButtons")

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
        self.tool_layout.addWidget(self.search)
        self.tool_layout.addWidget(self.search_btn)
        self.tool_layout.addStretch()
        self.tool_layout.addWidget(self.new_password_btn)
        self.tool_layout.addWidget(self.settings_btn)

        self.settings_btn.hide()

    def workspace_l(self): #left workspace widgets
        logger.debug("Left workspace successfully loaded! ✅")
        self.tree_view = QTreeView()         # Tree
        self.tree_view.setObjectName("LeftWorkspace")
        self.tree_view.setHeaderHidden(True) # Hide header 
        self.tree_view.setFixedWidth(250)    # Width
        self.tree_view.setEditTriggers(QTreeView.EditTrigger.NoEditTriggers) # Read only
        
        self.tree_model = QStandardItemModel()

        # Привязываем созданную модель к отображению
        self.tree_view.setModel(self.tree_model)

    def workspace_r(self): #right workspace widgets
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
        
        pixmap = QPixmap(self.config["view"]["welcome_logo"])
        
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
        self.db_size_lb = QLabel("Size database: ")
        self.db_size_lb.setStyleSheet("font-size: 16pt; border: 0px solid #111111;")
        self.db_creation_date = QLabel("Creation date: ")
        self.db_creation_date.setStyleSheet("font-size: 16pt; border: 0px solid #111111;")
        self.path_to_db = QLabel("Path to database: ")
        self.path_to_db.setStyleSheet("font-size: 16pt; border: 0px solid #111111;")
        self.db_count_passwords = QLabel("Database count passwords: ")
        self.db_count_passwords.setStyleSheet("font-size: 16pt; border: 0px solid #111111;")
        self.db_count_dublicate = QLabel("Database cound dublicate: ")
        self.db_count_dublicate.setStyleSheet("font-size: 16pt; border: 0px solid #111111;")
        self.db_login = QLabel("Login for database: ")
        self.db_login.setStyleSheet("font-size: 16pt; border: 0px solid #111111;")
        self.db_password = QLabel("Password for database: ")
        self.db_password.setStyleSheet("font-size: 16pt; border: 0px solid #111111;")

    def animations(self):
        
        def startup_animation(): #startup animations
            self.setWindowOpacity(self.config["view"]["window_opacity"])
            if self.config["view"]["window_startup_animations"]:
                self.startup_anim = QPropertyAnimation(self, b"windowOpacity")
                self.startup_anim.setDuration(800)          # Длительность в миллисекундах (0.8 сек)
                self.startup_anim.setStartValue(0.0)        # Начальное значение
                self.startup_anim.setEndValue(self.config["view"]["window_opacity"])          # Конечное значение
                self.startup_anim.setEasingCurve(QEasingCurve.Type.InOutQuad) # Плавность сглаживания
                self.startup_anim.start()
            else:
                return

        startup_animation()
