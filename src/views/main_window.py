from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from ..database import *
from .Dialogs.Create_New_Password import CreateNewPassword

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Настройки окна и стартовые запуски
        self.setWindowTitle("CastleKeys")     # title
        self.resize(900, 700)                 # start window size
        self.setMinimumSize(900, 700)         # minimum window size
        init_db()                             # init db
        self.init_ui()                        # load ui
        self.load_db()                        # load db

    def init_ui(self):                        # Elements Interface

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.workspace_container = QWidget()
        self.workspace_layout = QHBoxLayout()
        

    # Left workspace(Tree)
        self.tree_view = QTreeView()         # Tree
        self.tree_view.setHeaderHidden(True) # HeaderHidden
        self.tree_view.setFixedWidth(250)    # Width
        # self.tree_view.setEditTriggers(QTreeView.EditTrigger.NoEditTriggers) # Read only
        
        self.tree_model = QStandardItemModel()
        
        # Можно сделать еще один уровень вложенности:
        # item_nested = QStandardItem("Home")

        # Привязываем созданную модель к отображению
        self.tree_view.setModel(self.tree_model)
    
        
    # Right workspace
        self.right_layout = QVBoxLayout()
        self.right_container = QWidget()

        self.right_container.setStyleSheet("""
            background-color: #111111;
            border: 1px solid #222222;
            border-radius: 8px;
        """)

        # Заголовок пароля(название). Необходимо для визуального понимания того, какой пароль просматривает пользователь.
        self.title = QLabel("PM")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-size: 24pt; border: 0px solid #111111; background-color: #333;")
        label_font = self.title.font()
        label_font.setBold(True)
        self.title.setFont(label_font)

        # Название сервиса(google.com, telegram.org, instagram.com итд.)
        self.service_label = QLabel(f"Service: ") # тут нужно брать по названию из дерева 
        self.service_label.setStyleSheet("font-size: 16pt; border: 0px solid #111111;")

        # Логин для сервиса(email, номер телефона, можно добавить и то и то)  
        self.login_label = QLabel(f"Login: ")
        self.login_label.setStyleSheet("font-size: 16pt; border: 0px solid #111111;")

        # Пароль от сервиса
        self.password_label = QLabel(f"Password: ")
        self.password_label.setStyleSheet("font-size: 16pt; border: 0px solid #111111;")

        # Дата создания пароля
        # Логика в том, что у пользователя может быть несколько аккаунтов одного сервиса и дата создания пароля служит ориентиром. 
        self.creation_date_label = QLabel(f"Creation date: ")
        self.creation_date_label.setStyleSheet("font-size: 16pt; border: 0px solid #111111;")

        # Комментарий к паролю
        # Логика в том, что у пользователя может быть несколько аккаунто одного сервиса, быть аунтефикатор, чей аккаунт итд, комментарий служит ориетиром. 
        self.description_label = QLabel("Description:")
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_label.setStyleSheet("font-size: 16pt; border: 0px solid #111111;")
        self.description = QTextEdit()

        # TODO кнопка скрытия информации
        # Сделать кнопку для скрытия информации о пароле. Необходимо для людных мест и если рядом кто-то посторонний.
        # Логика в том, что при нажатии кнопки пароли мнгновенно скрываются, а для того, чтобы показать пароли нужно будет ввести пароль. В ИДЕАЛЕ СКРЫВАТЬ ПАРОЛИ ПОУМОЛЧАНИЮ И НЕ МЕНЯТЬ ПАРАМЕТР ВИДИМОСТИ. 

        # TODO Поле для комментариев
        # Сохранение заметки в реальном времени. 
        # Нужно сохранять заметку в памяти, а после закрытия программа доавит ее в базу данных, после чего при перезапуске будет читать заметку с базы данных. 


        self.right_layout.addWidget(self.title)
        self.right_layout.addWidget(self.service_label)
        self.right_layout.addWidget(self.login_label)
        self.right_layout.addWidget(self.password_label)
        self.right_layout.addWidget(self.creation_date_label)
        self.right_layout.addWidget(self.description_label)
        self.right_layout.addWidget(self.description)
        
        # hide on startup
        self.service_label.hide()
        self.login_label.hide()
        self.password_label.hide()
        self.creation_date_label.hide()
        self.description_label.hide()
        self.description.hide()
        

        self.right_layout.addStretch()

        self.right_container.setLayout(self.right_layout)

    # tool bar
        self.tool_container = QWidget()
        self.tool_layout = QHBoxLayout()

        self.tool_container.setStyleSheet("""
            background-color: #111111;
            border: 1px solid #222222;
            border-radius: 8px;
         """)

        self.new_button = QPushButton("New")
        self.new_button.setFixedSize(40, 30)

        self.edit_button = QPushButton("edit")
        self.edit_button.setFixedSize(40, 30)

        self.remove_button = QPushButton("remove")
        self.remove_button.setFixedSize(40, 30)

        self.settings_button = QPushButton("setting")
        self.settings_button.setFixedSize(40, 30)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search")
        self.search.setFixedSize(500, 30)

        self.search_button = QPushButton("search")
        self.search_button.setFixedSize(40, 30)
        

        self.tool_layout.addWidget(self.new_button)
        self.tool_layout.addWidget(self.edit_button)
        self.tool_layout.addWidget(self.remove_button)
        self.tool_layout.addStretch() 
        self.tool_layout.addWidget(self.search)
        self.tool_layout.addStretch() 
        self.tool_layout.addWidget(self.settings_button)

        self.tool_container.setLayout(self.tool_layout)
        #----------------------------------------------------------------------------------

        self.workspace_layout.addWidget(self.tree_view)
        self.workspace_layout.addWidget(self.right_container)

        main_layout = QVBoxLayout()
        
        main_layout.addWidget(self.tool_container)
        main_layout.addLayout(self.workspace_layout)
        self.central_widget.setLayout(main_layout)
    
    # Подгрузка паролей из базы данных и добавление их в дерево. 
    def load_db(self):
        data = get_all_passwords()
        
        self.tree_model.clear()
        
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
            self.login_text = row[2]
            self.password_text = row[3]
            self.date_text = row[4] if len(row) > 4 else "Unknown"
            # self.description = row[5]



            service_item = QStandardItem(self.service_text)
            
            service_item.setData(self.entry_id, Qt.ItemDataRole.UserRole)
            service_item.setData(self.login_text, Qt.ItemDataRole.UserRole + 1)
            service_item.setData(self.password_text, Qt.ItemDataRole.UserRole + 2)
            service_item.setData(self.date_text, Qt.ItemDataRole.UserRole + 3)

            self.root_item.appendRow(service_item)
            
        self.tree_view.expandAll()
            