import string
import secrets
from .models import Coupon  # assuming you have a Coupon model

def generate_coupon_code(length: int = 10) -> str:
    """
    Generate a unique alphanumeric coupon code.

    Args:
        length (int): Length of the coupon code. Defaults to 10.

    Returns:
        str: A unique coupon code.
    """
    characters = string.ascii_uppercase + string.digits

    while True:
        code = ''.join(secrets.choice(characters) for _ in range(length))
        # Ensure uniqueness by checking against the database
        if not Coupon.objects.filter(code=code).exists():
            return code
