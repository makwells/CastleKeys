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

    #config
    config_manager = ConfigManager()
    config = config_manager.load_config()
    
    db_path = config_manager.database_get_path() # path for database

    password_db = sqlite3.connect(db_path) # create and connect to a database
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


def add_password(service: str, url: str, login: str, password: str) -> int:
    logger.debug("function running")
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
    logger.debug("function running")
    global password_db

    if password_db is None:
        logger.error("Database not initialized!")
        return False

    try:
        cursor = password_db.cursor()

        cursor.execute(
            "DELETE FROM passwords WHERE id = ?",
            (password_id,)
        )

        deleted = cursor.rowcount > 0

        password_db.commit()
        cursor.close()

        if deleted:
            logger.success(f"Password ID {password_id} deleted")
        else:
            logger.warning(f"Password ID {password_id} not found")

        return deleted

    except sqlite3.Error as e:
        password_db.rollback()
        logger.error(f"Error deleting password: {e}")
        return False

def get_all_passwords() -> list:
    logger.debug("function running")
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

def get_count_passwords() -> int:
    logger.debug("function running")
    global password_db
    if password_db is None:
        logger.error("Database not initialized!")
        return 0
    try:
        cursor = password_db.cursor()
        cursor.execute("SELECT COUNT(*) FROM passwords")
        result = cursor.fetchone()
        password_count = result[0] if result else 0
        return password_count
    except sqlite3.Error as e:
        logger.error(f"Error fetching passwords: {e}")
        return 0

def update_password(password_id: int, service: str, url: str, login: str, password: str) -> bool:
    logger.debug("function running")
    global password_db
    
    if password_db is None:
        logger.error("Database not initialized!")
        return False
        
    try:
        cursor = password_db.cursor()
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
