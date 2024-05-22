import random
import string


def full_name(first_name: str, last_name: str):
    return f'{last_name} {first_name}'


def random_str(n: int) -> str:
    return ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(n)])
