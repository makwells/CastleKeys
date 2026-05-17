import sys
from PyQt6.QtWidgets import QApplication, QTabWidget, QWidget, QVBoxLayout, QLabel

class TabApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Горизонтальные вкладки')
        self.setGeometry(100, 100, 400, 250)

        main_layout = QVBoxLayout(self)

        # Создаем виджет вкладок
        tab_widget = QTabWidget(self)
        
        # Задаем горизонтальное расположение вкладок (слева или справа)
        tab_widget.setTabPosition(QTabWidget.TabPosition.West)

        # Добавляем вкладки с контентом
        for i in range(3):
            tab = QWidget()
            layout = QVBoxLayout(tab)
            layout.addWidget(QLabel(f'Содержимое вкладки {i+1}'))
            tab.setLayout(layout)
            tab_widget.addTab(tab, f'Вкладка {i+1}')

        main_layout.addWidget(tab_widget)
        self.setLayout(main_layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TabApp()
    ex.show()
    sys.exit(app.exec())
