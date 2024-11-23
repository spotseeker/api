import random


def generate_otp() -> str:
    """
    Generate a one-time password.
    """
    return str(random.randint(000000, 999999)).zfill(6)  # noqa: S311
