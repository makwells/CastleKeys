import sqlite3
from loguru import logger
from pathlib import Path

# Глобальное соединение (лучше позже вынести в класс)
password_db = None

def init_db():
    global password_db
    
    # Настройка логгера ОДИН раз при запуске
    logger.remove()
    logger.add(
        "logs/save_password.log",
        rotation="500 MB",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    )
    
    # Создаём папку для логов, если нет
    Path("logs").mkdir(exist_ok=True)
    
    # Подключение к БД
    password_db = sqlite3.connect("password.db")
    cursor = password_db.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Service TEXT NOT NULL,
            Login TEXT NOT NULL, 
            Password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    password_db.commit()
    logger.info("✅ Database initialized successfully")

def add_password(service: str, login: str, password: str) -> bool:
    """Добавляет запись в базу данных. Возвращает True при успехе."""
    global password_db
    
    if password_db is None:
        logger.error("❌ Database not initialized! Call init_db() first.")
        return False
    
    try:
        cursor = password_db.cursor()
        # Исправлено: Password (без s) и добавлен id
        cursor.execute(
            "INSERT INTO passwords (Service, Login, Password) VALUES (?, ?, ?)", 
            (service, login, password)
        )
        password_db.commit()  # commit() на ТОМ ЖЕ соединении
        logger.success(f"✅ Password for '{login}' ({service}) saved successfully")
        return True
        
    except sqlite3.IntegrityError as e:
        password_db.rollback()
        logger.error(f"❌ Integrity error (duplicate?): {e}")
        return False
    except sqlite3.OperationalError as e:
        password_db.rollback()
        logger.error(f"❌ Operational error: {e}")
        return False
    except sqlite3.Error as e:
        password_db.rollback()
        logger.error(f"❌ Unexpected database error: {e}")
        return False

def close_db():
    """Корректно закрывает соединение с БД."""
    global password_db
    if password_db:
        password_db.close()
        logger.info("🔌 Database connection closed")

# Для использования с context manager (опционально, более продвинутый вариант)
class Database:
    """Альтернатива глобальным переменным — ООП подход."""
    
    def __init__(self, db_path: str = "password.db"):
        self.db_path = db_path
        self.conn = None
        
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self._create_table()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type:  # Если было исключение — откат
                self.conn.rollback()
            self.conn.close()
        return False  # Не подавляем исключения
    
    def _create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Service TEXT NOT NULL,
                Login TEXT NOT NULL, 
                Password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()
    
    def add_password(self, service: str, login: str, password: str) -> bool:
        try:
            self.conn.execute(
                "INSERT INTO passwords (Service, Login, Password) VALUES (?, ?, ?)",
                (service, login, password)
            )
            self.conn.commit()
            logger.success(f"✅ Saved: {login}@{service}")
            return True
        except sqlite3.Error as e:
            logger.error(f"❌ DB error: {e}")
            return False
