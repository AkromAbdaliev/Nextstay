import smtplib

from app.core.config import settings
from app.tasks.celery import celery
from app.tasks.email import create_booking_confirmation


@celery.task
def send_booking_confirmation_email(booking: dict, email_to: str) -> None:
    email_to_mock = settings.SMTP_USER
    msg_content = create_booking_confirmation(booking, email_to_mock)

    with smtplib.SMTP(
        settings.SMTP_HOST, settings.SMTP_PORT
    ) as server:  # TLS connection used not SSL
        server.starttls()  # secure the connection
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)
