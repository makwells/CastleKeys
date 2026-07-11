# from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Window
        self.setWindowTitle("PM")     # title
        self.resize(900, 700)         # start window size
        self.setMinimumSize(900, 700) # minimum window size

        self._init_ui()               # load ui

    def new_category(self, name):
        category = QStandardItem(name)

    
    def _init_ui(self): # Elements Interface
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

        root_item = QStandardItem("Passwords") #Main item

        #BOLD FONT 
        #<----------------------------------->
        root_item_font = root_item.font()
        root_item_font.setBold(True)
        root_item.setFont(root_item_font)
        #<----------------------------------->
        
        self.tree_model.appendRow(root_item)
        
        # Создаем подкатегории (они будут вложены внутрь корневой)
        category_sites = QStandardItem("Sites")
        category_wifi = QStandardItem("Wi-Fi")
        category_other = QStandardItem("Other")
        
        # Добавляем подкатегории в корень дерева
        root_item.appendRow(category_sites)
        root_item.appendRow(category_wifi)
        root_item.appendRow(category_other)
        
        # Можно сделать еще один уровень вложенности:
        # item_nested = QStandardItem("Home")

        # Привязываем созданную модель к отображению
        self.tree_view.setModel(self.tree_model)
        
        # Автоматически разворачиваем дерево при старте
        self.tree_view.expandAll()
        #----------------------------------------------------------------------------------
        
        # Right workspace
        #----------------------------------------------------------------------------------
        right_container = QWidget()
        right_layout = QVBoxLayout()
        
        self.title = QLabel("PM")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-size: 24pt")

        right_layout.addWidget(self.title)

        right_layout.addStretch()
        right_container.setLayout(right_layout)
        #----------------------------------------------------------------------------------

        # tool bar
        #----------------------------------------------------------------------------------
        self.tool_container = QWidget()
        self.tool_layout = QHBoxLayout()

        self.new_button = QPushButton("New")
        self.new_button.setFixedSize(50, 40)
        
        self.edit_button = QPushButton("edit")
        self.edit_button.setFixedSize(50, 40)

        self.remove_button = QPushButton("remove")
        self.remove_button.setFixedSize(50, 40)

        self.settings_button = QPushButton("setting")
        self.settings_button.setFixedSize(50, 40)

        self.tool_layout.addWidget(self.new_button)
        self.tool_layout.addWidget(self.edit_button)
        self.tool_layout.addWidget(self.remove_button)
        self.tool_layout.addWidget(self.settings_button)

        self.tool_container.setLayout(self.tool_layout)
        #----------------------------------------------------------------------------------

        self.workspace_layout.addWidget(self.tree_view)
        self.workspace_layout.addWidget(right_container)

        main_layout = QVBoxLayout()
        
        main_layout.addWidget(self.tool_container)
        main_layout.addLayout(self.workspace_layout)
        self.central_widget.setLayout(main_layout)