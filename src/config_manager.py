#config_menager.py
import os
import sys
import toml
from pathlib import Path
import shutil
from src.setuplogger import *

class ConfigManager:
    def __init__(self, app_name: str="CastleKeys"):
        self.app_name = app_name
        self.config = self.config_path()

    def config_path(self):
        is_frozen = getattr(sys, "frozen", False)
        # если приложение скомпилировано
        if is_frozen:
            # если приложение запущено на windows
            if sys.platform == "win32":
                base_dir = Path(os.environ.get("APPDATA", Path.home())) / app_name
            # если приложение запущено на mac или linux
            else:
                base_dir = Path.home() / ".config" / self.app_name

            logger.debug(f"OS: {sys.platform}") 

            # создание файлов
            base_dir.mkdir(parents=True, exist_ok=True)    # создание конфигурационной папки проекта в ~/.config/CastleKeys
            user_config = base_dir / "config.toml"         # путь для пользовательского конфига

            #TODO создать папку в ~/.config/CastleKeys/themes и читать темы, для скомпилированного приложения от туда
            
            # user_themes = base_dir / "themes"              # путь для папки с темами
            # user_themes.mkdir(parents=True, exist_ok=True) # создание папки темы в ~/.config/CastleKeys/themes

            # создание конфига, если он еще не создан
            if not user_config.exists():  
                bundle_dir = Path(getattr(sys, "_MEIPASS", os.path.dirname(sys.argv[0])))
                default_config = bundle_dir / "config.toml"

                if default_config.exists():
                    # если дефолтный кофиг создан, то копировать его в папку с ~/.config
                    shutil.copy(default_config, user_config)
                else:
                    user_config.touch()
            return user_config
        
        # если приложение не скомпилировано, то конфиг будет читаться с корневой папки проекта. Режим разработки
        project_root = Path(sys.argv[0]).resolve().parent
        if project_root.name in ["models", "src"]:
            project_root = project_root.parent if project_root.name == "models" else project_root.parent.parent

        local_config = project_root / "config.toml"
        if not local_config.exists():
            local_config.touch()

        return local_config

    def load_config(self):
        try:
            with open(self.config, "r", encoding="utf-8") as config_file:
                return toml.load(config_file)
        except Exception as e:
            logger.error(f"Error reading config: {e}")

    @staticmethod
    def get_resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            # Путь внутри временной папки запущенного .app / .exe
            return os.path.join(sys._MEIPASS, relative_path)
        # Путь при обычном запуске скрипта во время разработки
        return os.path.abspath(relative_path)

    @staticmethod
    def _get_replacements():
        """Приватный метод: читает config и тему, возвращает словарь замен."""
        config_path = ConfigManager.get_resource_path("config.toml")
        with open(config_path, "r", encoding="utf-8") as config_file:
            config = toml.load(config_file)

        theme_filename = config["view"]["theme"]
        themes_dir = ConfigManager.get_resource_path("themes")
        theme_path = os.path.join(themes_dir, theme_filename)
        
        with open(theme_path, "r", encoding="utf-8") as theme_file:
            theme_data = toml.load(theme_file)

        replacements = {}
        for section_name, section_content in theme_data.items():
            if isinstance(section_content, dict):
                for key, value in section_content.items():
                    replacements[f"@{key}"] = value

        if "main" in theme_data:
            replacements["@background"] = theme_data["main"].get("background", "")
            replacements["@text"] = theme_data["main"].get("text", "")
            
        return replacements

    @staticmethod
    def _apply_replacements(template, replacements):
        """Приватный метод: применяет словарь замен к QSS-шаблону."""
        # Сортируем по длине, чтобы длинные маркеры заменились раньше коротких
        sorted_markers = sorted(replacements.keys(), key=len, reverse=True)
        for marker in sorted_markers:
            color = replacements[marker]
            if color:
                template = template.replace(marker, color)
        return template

    @staticmethod
    def _load_qss(primary_path, fallback_path):
        """Приватный метод: загружает QSS-файл, используя fallback, если основной не найден."""
        path = ConfigManager.get_resource_path(primary_path)
        if not os.path.exists(path):
            path = ConfigManager.get_resource_path(fallback_path)
        
        with open(path, "r", encoding="utf-8") as file:
            return file.read()

    @staticmethod
    def get_main_style():
        """Возвращает готовые стили для главного окна."""
        replacements = ConfigManager._get_replacements()
        template = ConfigManager._load_qss(
            os.path.join("src", "assets", "styles", "main_styles.qss"),
            os.path.join("assets", "styles", "main_styles.qss")
        )
        return ConfigManager._apply_replacements(template, replacements)

    @staticmethod
    def get_dialog_style():
        """Возвращает готовые стили для диалоговых окон."""
        replacements = ConfigManager._get_replacements()
        template = ConfigManager._load_qss(
            os.path.join("src", "assets", "styles", "dialog_styles.qss"),
            os.path.join("assets", "styles", "dialog_styles.qss")
        )
        return ConfigManager._apply_replacements(template, replacements)