from flask import Flask, render_template
from loguru import logger

# Создание логгера 
logger.remove()
logger.add("./logs/password_manager.log", rotation="500 MB")

app = Flask(__name__)

# Home page
# Отображение и поиск сохраенных паролей, переход на другие вкладки. 
@app.route("/")
def home():
    logger.info("Home page")
    return render_template("home.html")

# Generator page
#Генератор случайных паролей.
@app.route("/generator")
def generate_password():
    return render_template("generator.html")

# Settings page
# Настройка сайта. Отображение, сохранение паролей, тема оформления итд. 
@app.route("/settings")
def settings():
    logger.info("Settings page")
    return render_template("settings.html")

# Account page
# Настройка аккаунта: Фото профиля, пароль итд. 
@app.route("/account")
def account():
    logger.info("Account.html page")
    return render_template("account.html")


if __name__ == "__main__":
    logger.remove()
    logger.info("Password manager is running!")
    app.run(debug=True)
    