from PySide6.QtCore import *

class Search:
    #Signals
    search_text = Signal(dict)
    finished = Signal()

    def __init__(self, view):
        self._view = view #MainWindow
        self.search()

    def search(self):
        self._view.search_le.textChanged.connect(self.find) #MainWindow search bar

    def find(self):
        data = {"text": self._view.search_le.text().strip()}

        #send data
        if any(data.values()):
            self.search_text.emit(data)