from loguru import logger
import init_db

class Manage_Password_DB:
    def __init__(self):
        self.create_password()

    # Добавление пароля из базы данных
    def create_password(self):
        logger.remove()
        logger.add("logs/save_passwords.log", rotation="500 MB")
        
        # TODO Тут нужно получать значение из html страницы
        # --------------------------------------------------------
        self.service=  input("Service -> ")
        self.login=    input("Login ->")
        self.password= input("Password ->")
        # --------------------------------------------------------

        if self.service   is None: self.service  = "-"
        if self.login     is None: self.login    = "-"
        if self.password  is None: self.password = "-" 

        if self.service is None and self.login is None and self.password is None:
            print("Password is not saved!")
            logger.error("Password is not saved!")

            
        init_db.init_db()
        init_db.add_password(self.service, self.login, self.password)
    

    # Удаление пароля из базы данных
    def Remove_password(self):
        logger.remove()
        logger.add("logs/save_password.log", rotation="500 MB")


        # TODO Тут нужно получать значение из html страницы
        # --------------------------------------------------------
        self.remove_service=  input("Remove Service -> ")
        self.remove_login=    input("Remove Login ->")
        self.remove_password= input("Remove Password ->")
        # --------------------------------------------------------

        if self.remove_service is None: self.remove_service = "-"
        if self.remove_login is None: self.remove_login = "-"
        if self.remove_password is None: self.remove_password = "-" 

        if self.remove_service is None and self.remove_login is None and self.remove_password is None:
            print("Password is not removed!")
            logger.error("Password is not removed!")
        
        init_db.init_db()
        init_db.delete_password(self.remove_service, self.remove_login, self.remove_password)
            


if __name__ == "__main__":
    run = Manage_Password_DB()