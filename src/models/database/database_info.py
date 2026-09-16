#db_info.py
from pathlib import Path
from src.setuplogger import *
from src.models.database import database

class Database_info:
    def __init__(self):
        ...

        #TODO нужно писать дату создания бд 
        #TODO нужно писать количество дубликатов
        #TODO нужно писать логин и пароль от бд, чтобы в этой вкладке его можно было изменять.


    def db_size(self, path_to_db: str):
        database_size_btyes = Path(path_to_db).stat().st_size
        for unit in ['B', "KB", "MB", "GB", "TB"]:
            if database_size_btyes < 1024.0:
                return f"{database_size_btyes:.2f} {unit}"
            database_size_btyes /= 1024.0