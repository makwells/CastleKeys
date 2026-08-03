#main_wondow.py
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from ..database import *
from .Dialogs.create_new_password import CreateNewPassword
import json 
from ..setuplogger import setup_logger

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Config
        with open("config.json", "r") as config_file:
            logger.success("Config successfully loaded ✅")
            self.config = json.load(config_file)

        self.init_ui()                        # load ui
        self.load_db()                        # load db

    def init_ui(self):                        # Elements Interface
        logger.debug("Main Window successfully loaded! ✅")

        
        self.tool_bar()                       # Tool bar
        self.workspace_l()                    # Left workspace
        self.workspace_r()                    # Right workspace
            
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
    
    # Подгрузка паролей из базы данных и добавление их в дерево. 
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

        # FIXME добавление пароля в реальном времени
        # идея в том, чтобы при добавлении пароля хранить его в памяти компьютера, а после закрытия программы пароль добавлял в базу данных. При следующем запуске программа будет уже считывать пароль из базы данных. 

        
        # self.dialog_new_password = CreateNewPassword()
        # self.dialog_new_password.new_password_ui

        # input_service = self.dialog_new_password.input_service
        # input_login = self.dialog_new_password.input_login.text()
        # input_password = self.dialog_new_password.input_password.text()

        # self.root_item.appendRow(input_service)
        
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

    # TOOL BAR WIDGETS
    def tool_bar(self):
        logger.debug("Tool bar successfully loaded! ✅")
        self.app_title = QLabel("CastleKeys")
        self.app_title.setStyleSheet("border: 1px solid #111111; font-size: 24pt; font-weight: bold;")
        
        self.new_password_btn = QPushButton("New")
        self.new_password_btn.setFixedSize(40, 30)

        self.settings_btn = QPushButton("setting")
        self.settings_btn.setFixedSize(40, 30)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search")
        self.search.setFixedSize(500, 30)

        self.search_btn = QPushButton("search")
        self.search_btn.setFixedSize(40, 30)

        self.tool_container = QWidget()
        self.tool_layout = QHBoxLayout()

        self.tool_container.setStyleSheet("""
            background-color: #111111;
            border: 1px solid #222222;
            border-radius: 8px;
         """)
        tools = [
            self.app_title,
            self.tool_layout.addStretch(),
            self.search,
            self.search_btn,
            self.tool_layout.addStretch(),
            self.new_password_btn,
            self.settings_btn,
        ]
        for tool_bar_element in tools:
            self.tool_layout.addWidget(tool_bar_element)

    # LEFT WORKSPACE -> TREE
    def workspace_l(self): 
        logger.debug("Left workspace successfully loaded! ✅")
        self.tree_view = QTreeView()         # Tree
        self.tree_view.setHeaderHidden(True) # Hide header 
        self.tree_view.setFixedWidth(250)    # Width
        self.tree_view.setEditTriggers(QTreeView.EditTrigger.NoEditTriggers) # Read only
        
        self.tree_model = QStandardItemModel()

        # Привязываем созданную модель к отображению
        self.tree_view.setModel(self.tree_model)

    # RIGHT WORKSPACE
    def workspace_r(self):
        logger.debug("Right workspace successfully loaded! ✅")
        self.db_information()
         # NOTE Заголовок пароля(название). Необходимо для визуального понимания того, какой пароль просматривает пользователь.
        self.title = QLabel()
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-size: 24pt; border: 0px solid #111111; background-color: #333;")
        label_font = self.title.font()
        label_font.setBold(True)
        self.title.setFont(label_font)


        # SERVICE
        self.service_label = QLabel(f"Service: ")
        self.service_label.setStyleSheet("font-size: 16pt; border: 0px solid #111111;")

        #URL
        self.url_lb = QLabel("URL: ")
        self.url_lb.setStyleSheet("font-size: 16pt; border: 0px solid #111111;")


        # LOGIN 
        self.login_label = QLabel(f"Login: ")
        self.login_label.setStyleSheet("font-size: 16pt; border: 0px solid #111111;")


        # PASSWORD
        self.password_label = QLabel(f"Password: ")
        self.password_label.setStyleSheet("font-size: 16pt; border: 0px solid #111111;")


        # CREATION DATE
        # NOTE Логика в том, что у пользователя может быть несколько аккаунтов одного сервиса и дата создания пароля служит ориентиром. 
        self.creation_date_label = QLabel(f"Creation date: ")
        self.creation_date_label.setStyleSheet("font-size: 16pt; border: 0px solid #111111;")


        # DESCRIPTION
        self.description_label = QLabel("Description:")
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_label.setStyleSheet("font-size: 16pt; border: 0px solid #111111;")
        # NOTE Описание к паролю
        # Логика в том, что у пользователя может быть несколько аккаунто одного сервиса, быть аунтефикатор, чей-то аккаунт итд, описание служит ориетиром. Нужно при любом действии пользователя единожды сохранить описание.
        # Описание должно храниться в памяти компьютера при нажатии на другой пароль. При нажатии на другой пароль оно сохраняется в базу данных и при следующем заходе в программу считывает ее уже с базы данных.
        self.description = QTextEdit()


        # FIXME кнопка скрытия информации
        # Необходимо для людных мест и если рядом кто-то посторонний.
        # Логика в том, что при нажатии кнопки пароли мнгновенно скрываются, а для того, чтобы показать пароли нужно будет ввести пароль. В ИДЕАЛЕ СКРЫВАТЬ ПАРОЛИ ПОУМОЛЧАНИЮ И НЕ МЕНЯТЬ ПАРАМЕТР ВИДИМОСТИ. иконка глазика
        # Нужно сделать автоматическое скрытие при запуске программы
        # Нужно сделать поле ввода пароля при показе его снова.
        self.hide_password_btn = QPushButton("hide")
        self.hide_password_btn.setFixedSize(40, 40)
        self.hide_password_btn_state = False

        self.edit_password_btn = QPushButton("edit")
        self.edit_password_btn.setFixedSize(40, 40)

        self.del_password_btn = QPushButton("del")
        self.del_password_btn.setFixedSize(40, 40)

        self.right_layout = QVBoxLayout()
        self.under_title_layout = QHBoxLayout()


        self.right_container = QWidget()
        self.right_container.setStyleSheet("""
            background-color: #111111;
            border: 1px solid #222222;
            border-radius: 8px;
        """)
        

        # Right Workspace elements
        right_under_title_workspace_elements = [
            self.under_title_layout.addStretch(),
            self.hide_password_btn,
            self.edit_password_btn,
            self.del_password_btn
        ]
        right_workspace_elements = [
            self.title,
            self.service_label,
            self.url_lb,
            self.login_label,
            self.password_label,
            self.creation_date_label,
            self.description_label,
            self.description]
        right_workspace_db_information_elements = [
            self.db_size_lb,
            self.db_creation_date,
            self.path_to_db,
            self.db_count_passwords,
            self.db_count_dublicate,
            self.db_login,
            self.db_password

        ]

        #Добавление элементов right_under_title_workspace_elements
        for under_title_element in right_under_title_workspace_elements:
            self.under_title_layout.addWidget(under_title_element)

        self.hide_password_btn.hide()
        self.edit_password_btn.hide()
        self.del_password_btn.hide()

        # Добавление элементов right_workspace
        for index, right_layout_element in enumerate(right_workspace_elements):
            self.right_layout.addWidget(right_layout_element)
            right_layout_element.hide()
            if index == 0: self.right_layout.addLayout(self.under_title_layout)

        # Добавление элементов database_infromation
        for db_information_elements in right_workspace_db_information_elements:
            self.right_layout.addWidget(db_information_elements)
            db_information_elements.hide()
        
        self.title.show()

        self.right_layout.addStretch()

        self.right_container.setLayout(self.right_layout)


    # DATABASE INFORMATION WIDGETS
    def db_information(self):
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

