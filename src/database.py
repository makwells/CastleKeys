import sqlite3
from loguru import logger
from pathlib import Path

from src.setuplogger import setup_logger

# TODO нужно сделать хеширование паролей

password_db = None

def init_db():
    setup_logger()
    global password_db
        
    Path("logs").mkdir(exist_ok=True)
        
    password_db = sqlite3.connect("Passwords/passwords.db") # Папка с паролями
    cursor = password_db.cursor()
        
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Service TEXT NOT NULL,
                Login TEXT NOT NULL, 
                Password TEXT NOT NULL,
                Created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                Description TEXT
            )
        """)
    password_db.commit()
    logger.success("The database is connected.")
    
# Функция добавления пароля. 
def add_password(service: str, login: str, password: str) -> bool:
    setup_logger()

    global password_db
        
    if password_db is None:
        logger.error("Database not initialized! Call init_db() first")
        return False
        
    try:
        cursor = password_db.cursor()
        cursor.execute(
                "INSERT INTO passwords (Service, Login, Password) VALUES (?, ?, ?)", 
                (service, login, password)
        )
        password_db.commit()
        logger.success(f"Password for '{login}' ({service}) saved successfully")
        return True
            
    except sqlite3.IntegrityError as e:
        password_db.rollback()
        logger.error(f"Integrity error (duplicate?): {e}")
        return False
    except sqlite3.OperationalError as e:
        password_db.rollback()
        logger.error(f"Operational error: {e}")
        return False
    except sqlite3.Error as e:
        password_db.rollback()
        logger.error(f"Unexpected database error: {e}")
        return False

def delete_password(password_id: int) -> bool:
    setup_logger()

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
        cursor.execute("SELECT id, Service, Login, Password, Created_at FROM passwords")
        return cursor.fetchall() 
    except sqlite3.Error as e:
        logger.error(f"Error fetching passwords: {e}")
        return []


def close_db():
    global password_db
    if password_db:
        password_db.close()
        logger.success("The database has been successfully closed")
