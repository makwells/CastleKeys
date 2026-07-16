from ..views.Create_New_Password import CreateNewPassword
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

class MainController():
    def __init__(self, view):
        self._view  = view      #MainWindow

        self._connect_signals() #Signals

    def _connect_signals(self):
        
        self._view.tree_view.clicked.connect(self._on_category_clicked)         #tree select category
        self._view.new_button.clicked.connect(self._new_password_clicked)       #new password button
        self._view.edit_button.clicked.connect(self._edit_password_clicked)     #edit password button 
        self._view.remove_button.clicked.connect(self._remove_password_clicked) #remove password button 
        self._view.settings_button.clicked.connect(self._setting_clicked)       #settings button

    #select category
    def _on_category_clicked(self, index):
        item = self._view.tree_model.itemFromIndex(index)
        item_name = item.text()                                  #get text
        self._view.title.setText(f"{item_name}")                 #change title


        if item == self._view.root_item: # если выбран заголовок в пункте меню, то скрывать значения сервиса логина и пароля
            self._view.service_label.hide()
            self._view.login_label.hide()
            self._view.password_label.hide()
            self._view.creation_date_label.hide()
            return

        else: # если выбрано что-то иное то показывать
            self._view.service_label.show()
            self._view.login_label.show()
            self._view.password_label.show()
            self._view.creation_date_label.show()

        service_name = item.text()
        login = item.data(Qt.ItemDataRole.UserRole + 1)
        password = item.data(Qt.ItemDataRole.UserRole + 2)
        date = item.data(Qt.ItemDataRole.UserRole + 3)

        self._view.service_label.setText(f"Service: {service_name}")
        self._view.login_label.setText(f"Login: {login}")
        self._view.password_label.setText(f"Password: {password}")
        self._view.creation_date_label.setText(f"Creation date: {date}")        

    #add new password
    def _new_password_clicked(self):
        #open the child window to create a new password
        CreateNewPassword(self._view)
    
    #edit password
    def _edit_password_clicked(self):
        #open the child window to edit a password
        print('edit button')

    #remove password
    def _remove_password_clicked(self):
        #open the child window to remove a password
        print('remove button')
    
    def _setting_clicked(self):
        #open the child window for application settings
        print('setting button')
