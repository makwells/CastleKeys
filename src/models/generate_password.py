import random
import string

def generate_random_password(symbols=15):
    letters = string.ascii_letters + string.digits + string.punctuation
    generate = "".join(random.choices(letters, k=symbols))

    return generate