from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import toml

from src.config_manager import ConfigManager
from src.setuplogger import *

class SettingsController:
    def __init__(self, settings, view):
        self._settings = settings
        self._view = view
        
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()

        self._settings.startup_animations_cb.blockSignals(True)
        self._settings.startup_animations_cb.blockSignals(False)

        self._connect_signals()

    def _connect_signals(self):
        # Используем clicked, это надежнее, если toggled ведет себя странно
        self._settings.startup_animations_cb.checkStateChanged.connect(self.startup_animations)

    def startup_animations(self):
        logger.info("HELLO")
        is_checked = self._settings.startup_animations_cb.isChecked()

    #     # Меняем значение в словаре
    #     window_startup_animations_value = self.config["view"]["window_startup_animations"] = is_checked
    #     logger.info(f"{window_startup_animations_value}")

    #     # Перезаписываем файл
    
    #     logger.success(f"Файл успешно перезаписан! Новое значение: {is_checked}")
