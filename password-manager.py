import init_db             # database

from utils import settings # settings menu
from utils import edit     # edit mode menu
from utils import search   # search logic


import sys                 # system lib
from loguru import logger  # logger
import sqlite3
import qtawesome as qta    # icons

# UI
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class Password_Manager(QMainWindow):
    def __init__(self):
        super().__init__()

        logger.remove()
        logger.add(
            "logs/logs.log",
            rotation="500 MB",
            level="INFO",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
        )

        self.style_window = """

        background-color: #191919;
        color: #D3D3D3;
        """
        # Общий стиль кнопок
        self.style_button = """
        QPushButton{
        
        background-color: #515151;
        color: #D3D3D3;
        
        border: 1px solid #414141;
        border-radius: 10px;

        font-size: 14pt;
        font-weight: bold;
        }

        QPushButton:hover{
        background-color: #616161;
        border: 1px solid #888888;
        }

        QPushButton:pressed{
        background-color: #414141;
        border: 1px solid #888888;
        }
        """
        # Общий стиль поиска
        self.style_search = """
        QLineEdit{
        
        color: #ffffff;

        background-color: #414141;
        border: 1px solid #888888;
        
        border-radius: 5px; 

        font-size: 16pt;
        }

        QLineEdit:hover{
            background-color: #515151;
            border: 1px solid #414141;
        }
        """
        # Стиль заголовков таблицы
        self.style_HeaderView = """
        QHeaderView::section {
        background-color: #444444;

        border-bottom: 1px solid #ffffff;
        font-weight: bold;
        font-size: 14pt;
        }
        """
        # Стиль таблицы
        self.style_table  = """

        QTableWidget {
        background-color: #222222;
        selection-background-color: #333333;
        font-size: 16pt; 
        border: 1px solid #ffffff;
        gridline-color: #ffffff;
        }
        """
        
        self.style_tab = """
        
        """

        self.settings_window = None
        self.hide_passwords = False

        self.UI()                      # init UI
        logger.success("UI was successfully initialized")
        print("UI was successfully initialized")


        self.database_init_passwords() # init passwords database 
        logger.success("Database was successfully initialized")
        print("Database was successfully initialized")
            
    
    def UI(self): # Interface
        
        self.setWindowTitle("Password Manager") # Заголовок окна
        self.resize(650, 500)                   # Стартовые размеры окна
        self.setStyleSheet(self.style_window)   # Стили окна

        # Виджет вкладок
        tab_widget = QTabWidget()
        tab_widget.setTabPosition(QTabWidget.TabPosition.West) # Горизонтальные вкладки слева
        self.setCentralWidget(tab_widget)

        # tab_widget.setTabShape(QTabWidget.TabShape.Triangular)
        tab_widget.setDocumentMode(True)
        

        tab_widget.setStyleSheet("""
        background-color: #191919;
        """)

        # Контейнеры для вкладок
        tab_passwords = QWidget()
        tab_profile = QWidget()

        # Макет для вкладки "Пароли"
        passwords_layout = QVBoxLayout() 
        
        
        top_h_layout = QHBoxLayout() # Горизонтальный layout для поиска
        
        # Поиск
        search_bar = QLineEdit() 
        search_bar.setPlaceholderText("Search Password")
        search_bar.setFixedHeight(30) 
        search_bar.setStyleSheet(self.style_search)

        search_button = QPushButton()
        search_button.setIcon(qta.icon('fa5s.search', color='white'))
        search_button.setIconSize(QSize(24, 24))
        search_button.setFixedSize(30, 30) 
        search_button.setStyleSheet(self.style_button)

        top_h_layout.addWidget(search_bar)
        top_h_layout.addWidget(search_button)

        # Добавляем поиск в макет вкладки
        passwords_layout.addLayout(top_h_layout)
        
        # Панель управления под поиском
        center_layout = QHBoxLayout()

        passwords_label = QLabel("Мои пароли")
        passwords_label.setStyleSheet("font-size: 24pt; font-weight: bold;")

        settings_button = QPushButton()
        settings_button.setIcon(qta.icon('ri.settings-5-fill', color='white'))
        settings_button.setIconSize(QSize(24, 24))
        settings_button.setFixedSize(30, 30)
        settings_button.setStyleSheet(self.style_button)
        settings_button.clicked.connect(self.settings_win)
        
        new_password_button = QPushButton()
        new_password_button.setIcon(qta.icon('ei.plus', color='white'))
        new_password_button.setIconSize(QSize(24, 24))
        new_password_button.setFixedSize(30, 30)
        new_password_button.setStyleSheet(self.style_button)
        new_password_button.clicked.connect(self.add_password)

        edit_button = QPushButton()
        edit_button.setIcon(qta.icon('ri.edit-box-fill', color='white'))
        edit_button.setIconSize(QSize(24, 24))
        edit_button.setFixedSize(30, 30)
        edit_button.setStyleSheet(self.style_button)

        delete_button = QPushButton()
        delete_button.setIcon(qta.icon('ei.remove-sign', color='white'))
        delete_button.setIconSize(QSize(24, 24))
        delete_button.setFixedSize(30, 30)
        delete_button.setStyleSheet(self.style_button)
        delete_button.clicked.connect(self.del_password)

        center_layout.addWidget(passwords_label)
        center_layout.addStretch() 
        center_layout.addWidget(settings_button)
        center_layout.addWidget(new_password_button)
        center_layout.addWidget(edit_button)
        center_layout.addWidget(delete_button)

        # Добавляем панель управления в макет вкладки
        passwords_layout.addLayout(center_layout)

        # Таблица с паролями
        self.table = QTableWidget()
        self.row_count = 0
        self.table.setColumnCount(3)
        self.table.setRowCount(self.row_count+1)
        self.table.resizeRowsToContents()     
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setStyleSheet(self.style_HeaderView)

        self.table.setHorizontalHeaderLabels(["Service", "Login", "Password"])
        self.table.setStyleSheet(self.style_table)
        
        # Добавляем таблицу с паролями в макет вкладки
        passwords_layout.addWidget(self.table)

        # Привязываем весь настроенный макет к первой вкладке
        tab_passwords.setLayout(passwords_layout) 

        # Настраиваем вторую вкладку (Профиль), чтобы она не была пустой
        profile_layout = QVBoxLayout()
        profile_layout.addWidget(QLabel("Страница профиля и настроек"))
        profile_layout.addStretch()
        tab_profile.setLayout(profile_layout)

        tab_widget.addTab(tab_passwords, "Пароли")
        tab_widget.addTab(tab_profile, "Профиль")

    def database_init_passwords(self): # Загрузка паролей из базы данных в таблицу
        
        try:
            conn = sqlite3.connect('./data/passwords.db') # Подключение базы данных 
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM passwords") # Выбор таблицы 
            row = cursor.fetchall()

            item = QTableWidgetItem()

            for password_ in row:
                service = password_['Service']
                login = password_['Login']
                password = password_['Password']
                if self.hide_passwords == True:
                    password = "********"

                self.row_count += 1 
                self.table.setRowCount(self.row_count+1)

                self.table.setItem(self.row_count, 0, QTableWidgetItem(service))
                self.table.setItem(self.row_count, 1, QTableWidgetItem(login))
                self.table.setItem(self.row_count, 2, QTableWidgetItem(password))
        
        except Exception: 
            ...

        finally:
            conn.close()
    
    def add_password(self): # Форма добавления нового пароля
        # self.table.setRowCount(self.row_count+1)
        # Всплывающее окно добавления нового пароля
        new_password_window = QDialog(self)
        # Заголовок формы диалогового окна для добавления нового пароля
        new_password_window.setWindowTitle("New Password")
        # Размеры диалогового окна формы добавления нового пароля
        new_password_window.setFixedSize(350, 350)

        layout = QVBoxLayout(new_password_window)

        # Форма добавления названия сервиса
        service_input = QLineEdit()
        service_input.setStyleSheet(self.style_search)
        service_input.setPlaceholderText("Enter service name")

        # Форма доабвления логина
        login_input = QLineEdit()
        login_input.setStyleSheet(self.style_search)
        login_input.setPlaceholderText("Enter login or email")

        # Форма добавления пароля
        password_input = QLineEdit()
        password_input.setStyleSheet(self.style_search)
        password_input.setPlaceholderText("Enter password")

        # Добавление в лайоут 
        layout.addWidget(service_input)
        layout.addWidget(login_input)
        layout.addWidget(password_input)
        
        # Layout для кнопок
        button_layout = QHBoxLayout()
        
        # Кнопка сохранения нового пароля
        save_button = QPushButton("Save")
        save_button.setStyleSheet(self.style_button)
        
        # Кнопка отмены добавления пароля
        cancel_button = QPushButton("Cancel")
        cancel_button.setStyleSheet(self.style_button)

        # Добавление кнопок в layout
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        # Кнопка сохранения пароля
        save_button.clicked.connect(new_password_window.accept)
        save_button.setStyleSheet(self.style_button)
        save_button.setFixedHeight(30)

        # Кнопка отмены добавления нового пароля
        cancel_button.clicked.connect(new_password_window.reject)
        cancel_button.setStyleSheet(self.style_button)
        cancel_button.setFixedHeight(30)

        # Запуск диалога
        if new_password_window.exec() == QDialog.DialogCode.Accepted:

            # Получение текста из полей ввода  
            self.service = service_input.text().strip()
            self.login = login_input.text().strip()
            self.password = password_input.text().strip()
        
            # Если заполненны все поля, то сохранять пароль
            if self.service:
                # Добавление пароля в БД
                init_db.init_db()
                init_db.add_password(self.service, self.login, self.password)

                #---------------------------------------------
                    #TODO: Тут должно появляться сообщение о том, что пароль успешно добавлен
                #---------------------------------------------

                # Отображение добавленного пароля без перезапуска программы
                # Проверка строки, если строка занята, то пароль не будет заменять предыдущий, а будет переноситься на новую строку. 

                current_row_count = self.table.rowCount()
                self.table.insertRow(current_row_count)

                # Добавление пароля в таблицу
                self.table.setItem(current_row_count, 0, QTableWidgetItem(self.service))
                self.table.setItem(current_row_count, 1, QTableWidgetItem(self.login))
                self.table.setItem(current_row_count, 2, QTableWidgetItem(self.password))
                print(f"✅ Добавлен пароль для: {self.service}")

        # Срабатывает при нажатии кнопки "cancel"
        else:
            print("⛔ Добавление пароля отменено.")
    
    def del_password(self): # Удаление пароля

        # FIX при удалении первой строки, удаляются все оставльные
    #Удаление из таблицы(интерфейса)
        current_row = self.table.currentRow()
        if current_row > -1: 
            self.table.removeRow(current_row)
        current_row = self.table.currentRow()
    
    # Проверка: выбрана ли строка
        if current_row == -1:
            return 

        service_item = self.table.item(current_row, 0)
        if not service_item:
            return
        
        service_name = service_item.text()

        conn = sqlite3.connect('./data/passwords.db')
        cursor = conn.cursor()
        try:
            cursor.execute(
            "DELETE FROM passwords WHERE service = ?", 
            (service_name,)
            )
            conn.commit()
        
            self.table.removeRow(current_row)
        
        except sqlite3.Error as e:
            print(f"Ошибка при удалении: {e}")
        finally:
            conn.close()

    
    def settings_win(self):
        if self.settings_window is None:
            self.settings_window = settings.Settings_window()
        self.settings_window.show()
        

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = Password_Manager()
    window.show()

    app.exec()