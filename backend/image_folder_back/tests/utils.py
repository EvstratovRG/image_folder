import random
import string

def generate_random_string(length: int = 10) -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=length))
