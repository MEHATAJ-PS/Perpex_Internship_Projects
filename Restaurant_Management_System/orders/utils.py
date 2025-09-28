import secrets
import string
from .models import Order


def generate_unique_order_id(length: int = 8) -> str:
    """
    Generate a unique alphanumeric order ID.
    Ensures no collision with existing IDs in the DB.
    """
    characters = string.ascii_uppercase + string.digits
    while True:
        code = ''.join(secrets.choice(characters) for _ in range(length))
        if not Order.objects.filter(unique_id=code).exists():
            return code

