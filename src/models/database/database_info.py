#db_info.py
from pathlib import Path
from src.setuplogger import *

class Database_info:
    def __init__(self):

        # self.db_size("Passwords/passwords.db")
        ...

        #TODO нужно писать дату создания бд 
        #TODO нужно писать путь до бд 
        #TODO нужно писать количество паролей в бд 
        #TODO нужно писать количество дубликатов
        #TODO нужно писать логин и пароль от бд, чтобы в этой вкладке его можно было изменять.


    def db_size(self, path_to_db: str):
        database_size_btyes = Path(path_to_db).stat().st_size
        for unit in ['B', "KB", "MB", "GB", "TB"]:
            if database_size_btyes < 1024.0:
                return f"{database_size_btyes:.2f} {unit}"
            database_size_btyes /= 1024.0

    def get_path(self):
        ...
        # config_path = ConfigManager.get_resource_path("config.toml")
        # with open(config_path, "r", encoding="utf-8") as config_file:
        #     self.config = toml.load(config_file)

        


    
        
        

    
        