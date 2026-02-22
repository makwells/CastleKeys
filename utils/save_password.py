from loguru import logger
import init_db

class Save_Password:
    def __init__(self):
        self.type_password()
    
    def type_password(self):
        logger.remove()
        logger.add("logs/save_passwords.log", rotation="500 MB")
        self.service = "google"
        self.login = "w1nelex.08@gmail.com"
        self.password = "Makwells_8090"

        if self.service is None: self.service = "-"
        if self.login is None: self.login = "-"
        if self.password is None: self.password = "-" 

        if self.service is None and self.login is None and self.password is None:
            logger.error("Password is not saved!")

            
        init_db.init_db()
        init_db.add_password(self.service, self.login, self.password)


if __name__ == "__main__":
    run = Save_Password()