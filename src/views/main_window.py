#main_wondow.py
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from src.setuplogger import *
from src.config_manager import ConfigManager

from src.models.database.database import *

from src.views.ui.notifications.notifications_window import *
from src.views.ui.animations.animations import Animations

from src.views.ui.icons import icons_set_color
from src.views.ui.SideBar import SideBar
from src.views.ui.MenuBar import MenuBar
from src.views.ui.TopBar import TopBar



class MainWindow(QMainWindow):
    def __init__(self, pages):
        super().__init__()

        self.pages = pages # init pages 
        self.sidebar = SideBar(pages) # init sidebar
        self.topbar = TopBar() # init topbar
        self.menubar = MenuBar() # init menubar
        self.config_manager = ConfigManager() # init configuration

        
        # load config
        self.config = self.config_manager.load_config()
        logger.debug("Config successfully loaded ✅")
        
        # select themes dir
        self.themes_dir = self.config_manager.get_resource_path("themes/")
        self.current_theme = f"{self.themes_dir}{self.config["view"]["theme"]}"


        self.ui()                             # run ui
        self.apply_theme()                    # run theme

    def ui(self): #ui
        logger.debug("Main Window successfully loaded! ✅")

        self._animations()     # animations
        
        # Window and startup settings
        self.setWindowTitle("CastleKeys")     # title
        self.resize(900, 700)                 # start window size
        self.setMinimumSize(900, 700)         # minimum window size

        self.central_widget = QWidget()       # Central widget
        self.workspace_container = QWidget()
        self.workspace_layout = QHBoxLayout()
        main_layout = QVBoxLayout()

        self.setCentralWidget(self.central_widget)

        self.workspace_layout.addWidget(self.sidebar.sidebar_widget)
        self.workspace_layout.addWidget(self.pages)
        main_layout.addWidget(self.topbar.tool_container)
        main_layout.addLayout(self.workspace_layout)
        self.central_widget.setLayout(main_layout)
    
    def apply_theme(self): #theme
        try:
            style = self.config_manager.get_main_style()
            self.setStyleSheet(style)  
            logger.debug(f"Theme {self.current_theme} successfully applied to MainWindow ✅")
        except Exception as e:
            logger.error(f"Failed to apply theme {self.current_theme}: {e}")

    def workspace_left(self): #left workspace widgets
        logger.debug("Left workspace successfully loaded! ✅")

        self.left_container = QWidget()
        self.left_layout = QVBoxLayout()

        self.tree_view = QTreeView()         # Tree
        self.tree_view.setObjectName("LeftWorkspace")
        self.tree_view.setAnimated(True)     # opening animation
        self.tree_view.setHeaderHidden(True) # Hide header 
        self.tree_view.setFixedWidth(250)    # Width
        self.tree_view.setEditTriggers(QTreeView.EditTrigger.NoEditTriggers) # Read only

        #Tree
        self.tree_model = QStandardItemModel()
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.tree_model)
        self.tree_view.setModel(self.proxy_model)


        self.left_layout.addWidget(self.tree_view)

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
   