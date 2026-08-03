from loguru import logger
import sys

def setup_logger():

    # Очищаем дефотные настройки
    logger.remove()

    # Вывод в консоль
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{function}</cyan>:<blue>{line}</blue> - <level>{message}</level>",
        level="DEBUG"
    )

    # Запись логов в файл
    logger.add(
        "logs/CastleKeys.log",             # Путь к файлу (папка logs создастся сама)
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {function}:{line} - {message}",
        level="INFO",                      # В файл пишем только важные логи (без DEBUG)
        rotation="10 MB",                  # Создать новый файл, когда текущий достигнет 10 МБ
        retention="5 days",                # Удалять старые логи через 5 дней
        compression="zip",                 # Архивировать старые логи в zip для экономии места
        encoding="utf-8"                   # Поддержка кириллицы
    )