from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import logging

logger = logging.getLogger(__name__)

def send_email(recipient_email: str, subject: str, message: str, from_email: str = None) -> bool:
    """
    Sends an email using Django's email backend.

    Args:
        recipient_email (str): Recipient's email address.
        subject (str): Email subject.
        message (str): Email message body.
        from_email (str, optional): Sender email. Defaults to settings.DEFAULT_FROM_EMAIL.

    Returns:
        bool: True if email was sent successfully, False otherwise.
    """
    from_email = from_email or getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@example.com")

    try:
        # Validate email
        validate_email(recipient_email)
    except ValidationError:
        logger.error(f"Invalid recipient email: {recipient_email}")
        return False

    try:
        send_mail(subject, message, from_email, [recipient_email], fail_silently=False)
        return True
    except BadHeaderError:
        logger.error(f"Bad header found when sending email to {recipient_email}")
        return False
    except Exception as e:
        logger.error(f"Error sending email to {recipient_email}: {e}")
        return False


