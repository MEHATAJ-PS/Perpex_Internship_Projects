import logging
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from smtplib import SMTPException

logger = logging.getLogger(__name__)

def send_order_confirmation_email(order_id, customer_email, customer_name=None, items=None, total=None):
    """
    Sends an order confirmation email to the customer.

    Args:
        order_id (str | int): Unique order identifier.
        customer_email (str): Recipient's email address.
        customer_name (str, optional): Customer's name for personalization.
        items (list, optional): List of purchased items (str).
        total (float, optional): Total order amount.

    Returns:
        dict: {
            "success": bool,
            "message": str
        }
    """
    try:
        subject = f"Order Confirmation - #{order_id}"
        greeting = f"Hi {customer_name}," if customer_name else "Hello,"
        
        # Build order details string
        items_list = "\n".join(items) if items else "Items not available."
        total_display = f"Total Amount: ${total:.2f}" if total else "Total amount not specified."
        
        message = (
            f"{greeting}\n\n"
            f"Thank you for your order!\n\n"
            f"Order ID: {order_id}\n"
            f"Items:\n{items_list}\n\n"
            f"{total_display}\n\n"
            "We will notify you once your order is shipped.\n\n"
            "Best regards,\n"
            "Your Company Team"
        )

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[customer_email],
            fail_silently=False,
        )

        return {"success": True, "message": f"Order confirmation email sent to {customer_email}"}

    except BadHeaderError:
        logger.error(f"Invalid header found while sending email to {customer_email}")
        return {"success": False, "message": "Invalid header in email."}

    except SMTPException as e:
        logger.error(f"SMTP error while sending order confirmation email: {e}")
        return {"success": False, "message": "Failed to send email due to SMTP error."}

    except Exception as e:
        logger.exception(f"Unexpected error sending order confirmation email: {e}")
        return {"success": False, "message": "An unexpected error occurred while sending email."}
