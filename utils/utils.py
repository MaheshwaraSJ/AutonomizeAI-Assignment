import random


def generate_random_phone() -> str:

    first_digit = str(random.choice((6, 7, 8, 9)))
    remaining_digits = "".join(str(random.randint(0, 9)) for _ in range(9))
    return first_digit + remaining_digits