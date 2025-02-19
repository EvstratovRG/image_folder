import random
import string


def generate_random_string(length: int = 10) -> str:
    return "".join(
        random.choices(
            string.ascii_uppercase + string.ascii_lowercase + string.digits, k=length
        )
    )


def generate_random_valid_password(length: int = 10) -> str:
    random_symbol = random.choice(string.punctuation)
    random_high = random.choice(string.ascii_uppercase)
    random_digits = random.choice(string.digits)

    all_chars = string.ascii_letters + string.digits
    random_chars = random.choices(all_chars, k=length - 3)

    password_list = random_chars + [random_symbol] + [random_high] + [random_digits]

    random.shuffle(password_list)

    password = "".join(password_list)
    return password
