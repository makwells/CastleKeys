#database.py
import sqlite3
import os

from src.setuplogger import *
from src.config_manager import ConfigManager

# TODO нужно сделать хеширование паролей

password_db = None

def init_db():
    setup_logger()
    global password_db
    global config
        
    # Path("logs").mkdir(exist_ok=True)

    #config
    config_manager = ConfigManager()
    config = config_manager.load_config()

    db_dir = config["database"]["database_dir"]
    
    # if db_dir.startswith(".") or not db_dir.startswith("/"):
    #     home_dir = os.path.expanduser("~")
    #     db_dir = os.path.join(home_dir, ".castlekeys", db_dir.replace("./", ""))
    if not os.path.isabs(db_dir):
        db_dir = os.path.abspath(db_dir)

    # 3. Создаем структуру папок
    os.makedirs(db_dir, exist_ok=True)
    
    # 4. Формируем единый чистый путь к файлу базы данных
    db_path = os.path.join(db_dir, "passwords.db")

    # ИСПРАВЛЕНИЕ: Подключаемся строго по созданному db_path
    password_db = sqlite3.connect(db_path) 
    cursor = password_db.cursor()
        
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Service TEXT NOT NULL,
                URL TEXT,
                Login TEXT NOT NULL, 
                Password TEXT NOT NULL,
                Created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                Description TEXT
            )
        """)
    password_db.commit()
    logger.success("The database is connected ✅")


def add_password(service: str, url: str, login: str, password: str) -> int:
    global password_db
        
    if password_db is None:
        logger.error("Database not initialized! Call init_db() first")
        return -1
        
    try:
        cursor = password_db.cursor()
        cursor.execute(
                "INSERT INTO passwords (Service, URL, Login, Password) VALUES (?, ?, ?, ?)", 
                (service, url, login, password)
        )
        password_db.commit()
        
        # Получаем ID только что созданной записи
        new_id = cursor.lastrowid 
        logger.success(f"Password for '{service}' ({login}) saved successfully with ID {new_id}")
        return new_id
            
    except sqlite3.IntegrityError as e:
        password_db.rollback()
        logger.error(f"Integrity error (duplicate?): {e}")
        return -1
    except sqlite3.Error as e:
        password_db.rollback()
        logger.error(f"Database error: {e}")
        return -1

def delete_password(password_id: int) -> bool:

    global password_db
    if password_db is None: 
        return False
    try:
        cursor = password_db.cursor()
        # Удаляем строго одну запись по ее первичному ключу
        cursor.execute("DELETE FROM passwords WHERE id = ?", (password_id,))
        password_db.commit()
        cursor.close()
        return True
    except sqlite3.Error:
        password_db.rollback()
        return False

def get_all_passwords() -> list:
    global password_db
    if password_db is None:
        logger.error("Database not initialized!")
        return []
    try:
        cursor = password_db.cursor()
        cursor.execute("SELECT id, Service, URL, Login, Password, Created_at, Description FROM passwords")
        return cursor.fetchall() 
    except sqlite3.Error as e:
        logger.error(f"Error fetching passwords: {e}")
        return []

def update_password(password_id: int, service: str, url: str, login: str, password: str) -> bool:
    global password_db
    
    if password_db is None:
        logger.error("Database not initialized!")
        return False
        
    try:
        cursor = password_db.cursor()
        # Выполняем SQL-запрос UPDATE по конкретному id
        cursor.execute(
            """
            UPDATE passwords 
            SET Service = ?, URL = ?, Login = ?, Password = ? 
            WHERE id = ?
            """, 
            (service, url, login, password, password_id)
        )
        password_db.commit()
        cursor.close()
        return True
            
    except sqlite3.Error as e:
        password_db.rollback()
        logger.error(f"Error updating password ID {password_id}: {e}")
        return False
