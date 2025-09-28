import string
import secrets
from .models import Coupon  # adjust import if Coupon is in another app


def generate_coupon_code(length: int = 10) -> str:
    """
    Generate a unique alphanumeric coupon code.

    Args:
        length (int, optional): Length of the coupon code. Defaults to 10.

    Returns:
        str: A unique coupon code guaranteed not to collide with existing codes.
    """
    characters = string.ascii_uppercase + string.digits  # e.g. "AB12CD34"

    while True:
        code = ''.join(secrets.choice(characters) for _ in range(length))
        if not Coupon.objects.filter(code=code).exists():
            return code
