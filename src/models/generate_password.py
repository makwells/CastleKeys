#generate_passwords.py
import secrets
import string

def generate_random_password(symbols: int = 15) -> str:
    if symbols < 1:
        raise ValueError("Длина пароля должна быть больше нуля")

    alphabet = string.ascii_letters + string.digits + string.punctuation
    return "".join(secrets.choice(alphabet) for _ in range(symbols))