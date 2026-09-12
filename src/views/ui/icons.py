#icons.py
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from src.config_manager import ConfigManager
import os


def icons_set_color(icon_name: str, color_hex: str, size: QSize) -> QIcon:
    config_manager = ConfigManager()
    relative_path = os.path.join("src", "assets", "icons", icon_name)
    icon_path = config_manager.get_resource_path(relative_path)

    pixmap = QPixmap(icon_path).scaled(
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

