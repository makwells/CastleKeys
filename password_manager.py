from flask import Flask, render_template
from loguru import logger

logger.remove()
logger.add("./logs/password_manager.log", rotation="500 MB")

app = Flask(__name__ )


# Home page
# Отображение и поиск сохраенных паролей, переход на другие вкладки. 
@app.route("/")
def home():
    return render_template("index.html")

# Settings page
# Настройка сайта. Отображение, сохранение паролей, тема оформления итд. 
@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route("/account")
def account():
    return render_template("account.html"
    "")



if __name__ == "__main__":
    logger.remove()
    logger.info("Password manager is running!")
    app.run(debug=True)
    