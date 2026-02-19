"""Email delivery via SendGrid (optional fallback)."""

import logging

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from config import EMAIL_FROM, EMAIL_TO, SENDGRID_API_KEY

logger = logging.getLogger(__name__)


def send_email(subject: str, body_html: str) -> bool:
    """Send an email via SendGrid. Returns True on success."""
    if not all([SENDGRID_API_KEY, EMAIL_FROM, EMAIL_TO]):
        logger.error("Email not configured — set SENDGRID_API_KEY, EMAIL_FROM, EMAIL_TO")
        return False

    message = Mail(
        from_email=EMAIL_FROM,
        to_emails=EMAIL_TO,
        subject=subject,
        html_content=body_html,
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        logger.info("Email sent (status %s)", response.status_code)
        return True
    except Exception:
        logger.exception("Failed to send email")
        return False
