#icons.py
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
# from PyQt6.QtWidgets import QPushButton


def icons_set_color(icon_name: str, color_hex: str, size: QSize) -> QIcon:
    pixmap = QPixmap(f"src/assets/icons/{icon_name}").scaled(
    size, 
    Qt.AspectRatioMode.KeepAspectRatio, 
    Qt.TransformationMode.SmoothTransformation
)
    
    # 2. Создаем painter для перекраски
    painter = QPainter(pixmap)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), QColor(color_hex))
    painter.end()
    
    return QIcon(pixmap)

