import logging
from email_validator import validate_email, EmailNotValidError

# Configure logging (optional: can be customized in Django settings)
logger = logging.getLogger(__name__)


def is_valid_email(email: str) -> bool:
    """
    Validate an email address using the email-validator library.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if the email is valid, False otherwise.
    """
    try:
        # validate_email() returns a normalized email if valid
        validate_email(email)
        return True
    except EmailNotValidError as e:
        # Log the reason and return False
        logger.warning(f"Invalid email '{email}': {e}")
        return False
