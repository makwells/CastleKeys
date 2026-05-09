# from utils.init_db import init_db # database
import init_db

import sys
from loguru import logger
import sqlite3
import qtawesome as qta

# UI
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QHeaderView, QAbstractItemView, QMessageBox, QDialog, QLabel

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

        # Общий стиль кнопок
        self.style_button = """
        QPushButton{
        
        background-color: #515151;
        color: #fff;
        
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
        
        self.UI()                      # init UI
        logger.success("UI was successfully initialized")
        print("UI was successfully initialized")


        self.database_init_passwords() # init passwords database 
        logger.success("Database was successfully initialized")
        print("Database was successfully initialized")
            
    # Interface
    def UI(self):
        # Title
        self.setWindowTitle("Password Manager") 
        # window start size
        self.resize(650, 500)

        # Вертикальный layout
        main_layout = QVBoxLayout() 
                
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
        
        # Горизонтальный layout
        top_h_layout = QHBoxLayout() 

    # Search
        search_bar = QLineEdit() 
        search_bar.setPlaceholderText("Search Password")
        # Фиксированная высота поиска
        search_bar.setFixedHeight(30) 
        search_bar.setStyleSheet(self.style_search)

        # Добавление элемента в вертикальный layout
        # main_layout.addWidget(search_bar) 

        search_button = QPushButton()
        search_button.setIcon(qta.icon('fa5s.search', color='white'))
        search_button.setIconSize(QSize(24, 24))
        search_button.setFixedSize(30, 30) 
        search_button.setStyleSheet(self.style_button)

        top_h_layout.addWidget(search_bar)
        top_h_layout.addWidget(search_button)

        main_layout.addLayout(top_h_layout)
        

        center_layout = QHBoxLayout()

        passwords_label = QLabel("Passwords")
        passwords_label.setStyleSheet("font-size: 24pt; font-weight: bold;")
        

        settings_button = QPushButton()
        settings_button.setIcon(qta.icon('ri.settings-5-fill', color='white'))
        settings_button.setIconSize(QSize(24, 24))
        settings_button.setFixedSize(30, 30)
        settings_button.setStyleSheet(self.style_button)
        
        # Button new password   
        new_password_button = QPushButton()
        new_password_button.setIcon(qta.icon('ei.plus', color='white'))
        new_password_button.setIconSize(QSize(24, 24))
        new_password_button.setFixedSize(30, 30)
        new_password_button.setStyleSheet(self.style_button)
        new_password_button.clicked.connect(self.add_password)
        # layout.addStretch() # Пружина

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


        center_layout.addWidget(passwords_label)
        center_layout.addStretch() # Пружина
        center_layout.addWidget(settings_button)
        center_layout.addWidget(new_password_button)
        center_layout.addWidget(edit_button)
        center_layout.addWidget(delete_button)

        main_layout.addLayout(center_layout)

    # Table
        self.table = QTableWidget()

        self.row_count = 0

        # Количество Столбцов
        self.table.setColumnCount(3)
        # Количество строк
        self.table.setRowCount(self.row_count+1)
        # Авто-размер строк
        self.table.resizeRowsToContents()     

        # Запрет на редактирование ячеек
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        # Выделение сразу всей строки, а не отдельной ячейки
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        # Заголовки таблицы 
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setStyleSheet(self.style_HeaderView)

        self.table.setHorizontalHeaderLabels(["Service", "Login", "Password"])
        # Стиль заголовков таблицы 
        self.table.setStyleSheet(self.style_table)
        # Добавление таблицы в вертикальный layout
        main_layout.addWidget(self.table)
    

# Загрузка паролей из базы данных в таблицу
    def database_init_passwords(self):
        
        try:
            conn = sqlite3.connect('./data/passwords.db') # Подключение базы данных 
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor = conn.cursor()
            cursor.execute("SELECT * FROM passwords") # Выбор таблицы 
            row = cursor.fetchall()

            for password_ in row:
                service = password_['Service']
                login = password_['Login']
                password = password_['Password']

                self.table.setItem(self.row_count, 0, QTableWidgetItem(service))
                self.table.setItem(self.row_count, 1, QTableWidgetItem(login))
                self.table.setItem(self.row_count, 2, QTableWidgetItem(password))

                self.row_count += 1 
                self.table.setRowCount(self.row_count+1)
        
        except Exception: 
            ...

# ФОРМА ДОБАВЛЕНИЯ НОВОГО ПАРОЛЯ
    def add_password(self):
        self.table.setRowCount(self.row_count+1)
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
                # TODO: Логика сохранения пароля
                # Нужно сделат добавление в бд и из бд сделать так, чтобы читалась таблица и добавлялась в интерфейс, но при этом при добавление пароля сделать так, чтобы не перезапуская новый пароль тоже отображался. 

                # Добавление пароля в БД
                init_db.init_db()
                init_db.add_password(self.service, self.login, self.password)

                #---------------------------------------------
                    # #TODO: Тут должно появляться сообщение о том, что пароль успешно добавлен
                #---------------------------------------------

                # Отображение добавленного пароля без перезапуска программы
                # Проверка строки, если строка занята, то пароль не будет заменять предыдущий, а будет переноситься на новую строку. 
                target_row = -1 
                for row in range(self.table.rowCount()):
                    item = self.table.item(row, 1)

                    if item is None or item.text() == "":
                        target_row = row
                        break 
                if target_row == -1: 
                    target_row = self.table.rowCount()
                    self.table.insertRow(target_row)

                # Добавление пароля в таблицу
                self.table.setItem(target_row, 0, QTableWidgetItem(self.service))
                self.table.setItem(target_row, 1, QTableWidgetItem(self.login))
                self.table.setItem(target_row, 2, QTableWidgetItem(self.password))
                print(f"✅ Добавлен пароль для: {self.service}")

        # Срабатывает при нажатии кнопки "cancel"
        else:
            print("⛔ Добавление пароля отменено.")

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = Password_Manager()
    window.show()

    app.exec()