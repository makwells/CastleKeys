from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import toml

class SettingsController:
    def __init__(self, settings, view):
        self._settings = settings
        self._view = view
        
        # 1. Загружаем конфигурацию
        try:
            with open("config.toml", "r", encoding="utf-8") as config_file:
                self.config = toml.load(config_file)
        except FileNotFoundError:
            self.config = {"view": {"startup_animations": True}}

        # 2. Извлекаем текущее состояние
        current_state = self.config.get("view", {}).get("startup_animations", True)

        # ВАЖНО: Блокируем сигналы на время установки значения, 
        # чтобы чекбокс при старте сам себя не перезаписывал
        self._settings.startup_animations_cb.blockSignals(True)
        self._settings.startup_animations_cb.setChecked(current_state)
        self._settings.startup_animations_cb.blockSignals(False)

        # 3. Подключаем сигналы
        self._connect_signals()

    def _connect_signals(self):
        # Используем clicked, это надежнее, если toggled ведет себя странно
        self._settings.startup_animations_cb.clicked.connect(self._startup_animations)

    def _startup_animations(self):
        # Получаем РЕАЛЬНОЕ состояние чекбокса прямо в момент клика
        is_checked = self._settings.startup_animations_cb.isChecked()

        # Проверяем и создаем секцию, если её не было
        if "view" not in self.config:
            self.config["view"] = {}

        # Меняем значение в словаре
        self.config["view"]["startup_animations"] = is_checked

        # Перезаписываем файл
        with open("config.toml", "w", encoding="utf-8") as f:
            toml.dump(self.config, f)
            
        print(f"Файл успешно перезаписан! Новое значение: {is_checked}")
