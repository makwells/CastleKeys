from ..views.Create_New_Password import CreateNewPassword

class MainController():
    def __init__(self, view):
        # self._model = model #database model
        self._view  = view

        self._connect_signals()

    def _connect_signals(self):
        #tree category
        self._view.tree_view.clicked.connect(self._on_category_clicked)
        #new password button
        self._view.new_button.clicked.connect(self._new_password_clicked) 
        #edit password button 
        self._view.edit_button.clicked.connect(self._edit_password_clicked)
        #remove password button 
        self._view.remove_button.clicked.connect(self._remove_password_clicked)
        #settings button
        self._view.settings_button.clicked.connect(self._setting_clicked)

    #select category
    def _on_category_clicked(self, index):
        self.category_name = self._view.tree_model.itemFromIndex(index).text() #get text
        self._view.title.setText(f"{self.category_name}")                      #change title

    #add new password
    def _new_password_clicked(self):
        #open the child window to create a new password
        # print('new button') 
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
