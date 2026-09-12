import os
import sys
import toml
from pathlib import Path
import shutil
from src.setuplogger import logger

class ConfigManager:
    def __init__(self):
        self.bundle_dir = Path(getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(sys.argv[0]))))
        self.config = self._get_config_path()
        self.theme_path = self._get_theme_path()

    def _get_config_path(self):
        # 1. Определяем базовые директории в зависимости от ОС
        if sys.platform == "win32":
            self.base_dir = Path(os.environ.get("APPDATA", Path.home())) / "CastleKeys"
        elif sys.platform == "darwin":  # macOS
            self.base_dir = Path.home() / "Library" / "Application Support" / "CastleKeys"
        else:  # Linux
            self.base_dir = Path.home() / ".config" / "CastleKeys"
            
        self.source_dir = self.base_dir  # БД и конфиг храним в одной базовой директории

        # 2. Создаем директории
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.source_dir.mkdir(parents=True, exist_ok=True)

        # 3. Логика копирования дефолтного конфига
        user_config = self.base_dir / "config.toml"
        
        if not user_config.exists():
            default_config = self.bundle_dir / "config.toml"
            if default_config.exists():
                shutil.copy(default_config, user_config)
                logger.success("Config.toml has been successfully created from bundle")
            else:
                # Fallback для режима разработки, если в bundle нет
                dev_config = Path(__file__).resolve().parent.parent / "config.toml"
                if dev_config.exists():
                    shutil.copy(dev_config, user_config)
                    logger.success("Config.toml has been successfully created from dev folder")
                else:
                    user_config.touch()
                    logger.warning("Created empty config.toml")
                    
        return user_config

    def database_get_path(self):
        user_database = self.source_dir / "passwords.db"
        if not user_database.exists():
            logger.success("Database will be created on first use")
        else:
            logger.info("Database already exists")
        return user_database

    def _get_theme_path(self):
        themes_dir = self.base_dir / "themes"
        themes_dir.mkdir(parents=True, exist_ok=True)

        user_dark_theme = themes_dir / "dark.toml"
        user_light_theme = themes_dir / "light.toml"

        # Копируем темы из bundle или dev-окружения, если их нет
        for theme_name, user_theme_path in [("dark.toml", user_dark_theme), ("light.toml", user_light_theme)]:
            if not user_theme_path.exists():
                default_theme = self.bundle_dir / "themes" / theme_name
                if not default_theme.exists():
                    # Fallback для разработки
                    default_theme = Path(__file__).resolve().parent.parent / "themes" / theme_name
                
                if default_theme.exists():
                    shutil.copy(default_theme, user_theme_path)
                    logger.success(f"{theme_name} has been successfully created")
                else:
                    user_theme_path.touch()
                    logger.warning(f"Created empty {theme_name}")

        # TODO: В будущем здесь можно читать config["view"]["theme"] и возвращать нужную тему
        # Пока возвращаем темную по умолчанию
        return user_dark_theme

    def load_config(self):
        try:
            with open(self.config, "r", encoding="utf-8") as config_file:
                return toml.load(config_file)
        except Exception as e:
            logger.error(f"Error reading config: {e}")
            return {}

    def get_resource_path(self, relative_path):
        """Возвращает абсолютный путь к ресурсу, учитывая сборку PyInstaller."""
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.abspath(relative_path)

    def _get_replacements(self):
        """Приватный метод: читает config и тему, возвращает словарь замен."""
        config_data = self.load_config()
        
        try:
            with open(self.theme_path, "r", encoding="utf-8") as theme_file:
                theme_data = toml.load(theme_file)
        except Exception as e:
            logger.error(f"Error reading theme file {self.theme_path}: {e}")
            theme_data = {}

        replacements = {}
        for section_name, section_content in theme_data.items():
            if isinstance(section_content, dict):
                for key, value in section_content.items():
                    replacements[f"@{key}"] = str(value)

        if "main" in theme_data:
            replacements["@background"] = str(theme_data["main"].get("background", ""))
            replacements["@text"] = str(theme_data["main"].get("text", ""))
            
        return replacements

    def _apply_replacements(self, template, replacements):
        """Приватный метод: применяет словарь замен к QSS-шаблону."""
        # Сортируем по длине, чтобы длинные маркеры заменились раньше коротких
        sorted_markers = sorted(replacements.keys(), key=len, reverse=True)
        for marker in sorted_markers:
            color = replacements[marker]
            if color:
                template = template.replace(marker, color)
        return template

    def _load_qss(self, fallback_path):
        """Приватный метод: загружает QSS-файл."""
        path = self.get_resource_path(fallback_path)
        if not os.path.exists(path):
            logger.error(f"QSS file not found: {path}")
            return ""
        
        with open(path, "r", encoding="utf-8") as file:
            return file.read()

    def get_main_style(self):
        """Возвращает готовые стили для главного окна."""
        replacements = self._get_replacements()
        template = self._load_qss(os.path.join("src", "assets", "styles", "main_styles.qss"))
        return self._apply_replacements(template, replacements)

    def get_dialog_style(self):
        """Возвращает готовые стили для диалоговых окон."""
        replacements = self._get_replacements()
        template = self._load_qss(os.path.join("src", "assets", "styles", "dialog_styles.qss"))
        return self._apply_replacements(template, replacements)