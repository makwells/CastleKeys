#theme_manager
import os
import sys
import toml

class ConfigManager:
    @staticmethod
    @staticmethod
    def get_style():
        # 1. Читаем конфиг
        config_path = ConfigManager.get_resource_path("config.toml")
        with open(config_path, "r", encoding="utf-8") as config_file:
            config = toml.load(config_file)

        theme_filename = config["view"]["theme"]

        # 2. Путь к темам
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

        # 3. ИСПРАВЛЕНИЕ: Убираем "src" из пути, так как папка assets лежит внутри распакованной "src"
        qss_path = ConfigManager.get_resource_path(os.path.join("src", "assets", "styles", "main_styles.qss"))
        
        # Если код выше всё равно выдает пустой стиль, попробуйте альтернативный путь без первого "src":
        if not os.path.exists(qss_path):
            qss_path = ConfigManager.get_resource_path(os.path.join("assets", "styles", "main_styles.qss"))

        with open(qss_path, "r", encoding="utf-8") as styles_file:
            qss_template = styles_file.read()

        sorted_markers = sorted(replacements.keys(), key=len, reverse=True)

        for marker in sorted_markers:
            color = replacements[marker]
            if color:
                qss_template = qss_template.replace(marker, color)

        return qss_template


    def get_resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            # Путь внутри временной папки запущенного .app / .exe
            return os.path.join(sys._MEIPASS, relative_path)
        # Путь при обычном запуске скрипта во время разработки
        return os.path.abspath(relative_path)