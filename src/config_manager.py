# theme_manager
# import os
# import sys
# import toml

# class ConfigManager:
#     @staticmethod
#     def get_style():
#         config_path = ConfigManager.get_resource_path("config.toml")
#         with open(config_path, "r", encoding="utf-8") as config_file:
#             config = toml.load(config_file)

#         theme_filename = config["view"]["theme"]

#         # Themes folder
#         themes_dir = ConfigManager.get_resource_path("themes")
#         theme_path = os.path.join(themes_dir, theme_filename)
        
#         with open(theme_path, "r", encoding="utf-8") as theme_file:
#             theme_data = toml.load(theme_file)

#         replacements = {}
#         for section_name, section_content in theme_data.items():
#             if isinstance(section_content, dict):
#                 for key, value in section_content.items():
#                     replacements[f"@{key}"] = value

#         if "main" in theme_data:
#             replacements["@background"] = theme_data["main"].get("background", "")
#             replacements["@text"] = theme_data["main"].get("text", "")

#         #main_styles.qss
#         main_qss_path = ConfigManager.get_resource_path(os.path.join("src", "assets", "styles", "main_styles.qss"))

#         #dialog.qss
#         dialogs_qss_path = ConfigManager.get_resource_path(os.path.join("src", "assets", "styles", "dialog_styles.qss"))
        
#         # alternative method for a main_qss_path, if up code returned empty style
#         if not os.path.exists(main_qss_path):
#             main_qss_path = ConfigManager.get_resource_path(os.path.join("assets", "styles", "main_styles.qss"))

#         # alternative method for a dialog_qss_path, if up code returned empty style
#         if not os.path.exists(dialogs_qss_path):
#             dialogs_qss_path = ConfigManager.get_resource_path(os.path.join("assets", "styles", "dialog_styles.qss"))

        
#         # alternative method for a dialog_qss_path, if up code returned empty style
#         if not os.path.exists(dialogs_qss_path):
#             dialogs_qss_path = ConfigManager.get_resource_path(os.path.join("assets", "styles", "dialog_styles.qss"))

        
#         with open(main_qss_path, "r", encoding="utf-8") as main_styles_file:
#             main_qss_template = main_styles_file.read()
#         with open(dialogs_qss_path, "r", encoding="utf-8") as dialog_styles_file:
#             dialog_qss_template = dialog_styles_file.read()

#         sorted_markers = sorted(replacements.keys(), key=len, reverse=True)

#         for marker in sorted_markers:
#             color = replacements[marker]
#             if color:
#                 main_qss_template = main_qss_template.replace(marker, color)

#         for marker in sorted_markers:
#             color = replacements[marker]
#             if color:
#                 dialog_qss_template = dialog_qss_template.replace(marker, color)

#         return main_qss_template




#     def get_resource_path(relative_path):
#         if hasattr(sys, '_MEIPASS'):
#             # Путь внутри временной папки запущенного .app / .exe
#             return os.path.join(sys._MEIPASS, relative_path)
#         # Путь при обычном запуске скрипта во время разработки
#         return os.path.abspath(relative_path)

#     def load_config():
#         config_path = ConfigManager.get_resource_path("config.toml")
#         with open(config_path, "r", encoding="utf-8") as config_file:
#             config = toml.load(config_file)









import os
import sys
import toml

class ConfigManager:
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

    @staticmethod
    def load_config():
        config_path = ConfigManager.get_resource_path("config.toml")
        with open(config_path, "r", encoding="utf-8") as config_file:
            return toml.load(config_file) # Добавлен return, иначе метод ничего не возвращал