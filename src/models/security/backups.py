import zipfile
from datetime import datetime
from src.config_manager import ConfigManager

def backup():
    current_date = datetime.now().strftime("%Y-%m-%d|%H:%M")
    with zipfile.ZipFile(f"Backups/backup-{current_date}.zip", "w", compression=zipfile.ZIP_DEFLATED) as backup_archive:
        backup_archive.write("config.toml")
        backup_archive.write("Passwords/passwords.db")
        backup_archive.write("themes/dark.toml")


def backup_timer():
    config_manager = ConfigManager()
    config = config_manager.load_config()

    #day check 
    if datetime.now().day == config["database"]["backup_day"]:
        backup()
 