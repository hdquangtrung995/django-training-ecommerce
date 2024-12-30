import random
import string


def find(condition, iterable):
    """
    Find the first element in 'iterable' that satisfies 'condition' function.
    Returns None if no such element is found.
    """
    return next((item for item in iterable if condition(item)), None)


def find_index(condition, iterable):
    """
    Find the index of the first element in 'iterable' that satisfies 'condition' function.
    Returns -1 if no such element is found.
    """
    return next((i for i, item in enumerate(iterable) if condition(item)), -1)


def generate_sku(length=8, prefix="", suffix=""):
    """
    Generate a random SKU.

    Args:
        length (int): Length of the random part of the SKU (default is 8).
        prefix (str): Optional prefix for the SKU.
        suffix (str): Optional suffix for the SKU.

    Returns:
        str: A randomly generated SKU.
    """
    random_part = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=length)
    )
    return f"{prefix}{random_part}{suffix}"
