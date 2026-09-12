#setuplogger.py
from loguru import logger
import sys

def setup_logger():

    # clear settings 
    logger.remove()

    # output console
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <red>{file}</red>:<cyan>{function}</cyan>:<blue>{line}</blue> - <level>{message}</level>",
        level="DEBUG"
    )

    # write file 
    logger.add(
        "logs/CastleKeys.log",             # Путь к файлу (папка logs создастся сама)
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {file}:{function}:{line} - {message}",
        level="INFO",                      # В файл пишем только важные логи (без DEBUG)
        rotation="10 MB",                  # Создать новый файл, когда текущий достигнет 10 МБ
        retention="5 days",                # Удалять старые логи через 5 дней
        compression="zip",                 # Архивировать старые логи в zip для экономии места
        encoding="utf-8"                   # Поддержка кириллицы
    )