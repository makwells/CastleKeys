from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from ..database import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Window
        self.setWindowTitle("PM")     # title
        self.resize(900, 700)         # start window size
        self.setMinimumSize(900, 700) # minimum window size
        init_db()                     # init db
        self.init_ui()                # load ui
        self.load_db()                # load db

    def init_ui(self): # Elements Interface

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.workspace_container = QWidget()
        self.workspace_layout = QHBoxLayout()
        

        # Left workspace(Tree)
        #----------------------------------------------------------------------------------
        self.tree_view = QTreeView()         # Tree
        self.tree_view.setHeaderHidden(True) # HeaderHidden
        self.tree_view.setFixedWidth(250)    # Width
        self.tree_view.setEditTriggers(QTreeView.EditTrigger.NoEditTriggers) # Read only
        
        self.tree_model = QStandardItemModel()
        
        # Можно сделать еще один уровень вложенности:
        # item_nested = QStandardItem("Home")

        # Привязываем созданную модель к отображению
        self.tree_view.setModel(self.tree_model)
        
        #----------------------------------------------------------------------------------
        
        # Right workspace
        #----------------------------------------------------------------------------------
        self.right_container = QWidget()
        self.right_layout = QVBoxLayout()
        

        self.right_container.setStyleSheet("""
            background-color: #111111;
            border: 1px solid #222222;
            border-radius: 8px;
        """)

        self.title = QLabel("PM")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-size: 24pt; border: 0px solid #111111;")
        label_font = self.title.font()
        label_font.setBold(True)
        self.title.setFont(label_font)

        self.service_label = QLabel(f"Service: ") # тут нужно брать по названию из дерева 
        self.service_label.setStyleSheet("font-size: 16pt; border: 0px solid #111111;")

        self.login_label = QLabel(f"Login: ")
        self.login_label.setStyleSheet("font-size: 16pt; border: 0px solid #111111;")

        self.password_label = QLabel(f"Password: ")
        self.password_label.setStyleSheet("font-size: 16pt; border: 0px solid #111111;")

        self.creation_date_label = QLabel(f"Creation date: ")
        self.creation_date_label.setStyleSheet("font-size: 16pt; border: 0px solid #111111;")

        # TODO нужно добавить поле для комментариев

        self.right_layout.addWidget(self.title)
        self.right_layout.addWidget(self.service_label)
        self.right_layout.addWidget(self.login_label)
        self.right_layout.addWidget(self.password_label)
        self.right_layout.addWidget(self.creation_date_label)
        
        # hide on startup
        self.service_label.hide()
        self.login_label.hide()
        self.password_label.hide()
        self.creation_date_label.hide()
        

        self.right_layout.addStretch()

        self.right_container.setLayout(self.right_layout)
        #----------------------------------------------------------------------------------

        # tool bar
        #----------------------------------------------------------------------------------
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
        self.search.setFixedHeight(30)

        self.tool_layout.addWidget(self.new_button)
        self.tool_layout.addWidget(self.edit_button)
        self.tool_layout.addWidget(self.remove_button)
        self.tool_layout.addWidget(self.settings_button)
        self.tool_layout.addStretch() 
        self.tool_layout.addWidget(self.search)
        self.tool_container.setLayout(self.tool_layout)
        #----------------------------------------------------------------------------------

        self.workspace_layout.addWidget(self.tree_view)
        self.workspace_layout.addWidget(self.right_container)

        main_layout = QVBoxLayout()
        
        main_layout.addWidget(self.tool_container)
        main_layout.addLayout(self.workspace_layout)
        self.central_widget.setLayout(main_layout)
    
    def load_db(self):
        data = get_all_passwords()
        
        self.tree_model.clear()
        
        self.root_item = QStandardItem("Passwords")
        root_item_font = self.root_item.font()
        root_item_font.setBold(True)
        self.root_item.setFont(root_item_font)
        
        self.tree_model.appendRow(self.root_item)

        for row in data:
            self.entry_id = row[0]
            self.service_text = row[1]
            self.login_text = row[2]
            self.password_text = row[3]

            self.date_text = row[4] if len(row) > 4 else "Unknown"

            service_item = QStandardItem(self.service_text)
            
            service_item.setData(self.entry_id, Qt.ItemDataRole.UserRole)
            service_item.setData(self.login_text, Qt.ItemDataRole.UserRole + 1)
            service_item.setData(self.password_text, Qt.ItemDataRole.UserRole + 2)
            service_item.setData(self.date_text, Qt.ItemDataRole.UserRole + 3)

            self.root_item.appendRow(service_item)
            
        self.tree_view.expandAll()
            