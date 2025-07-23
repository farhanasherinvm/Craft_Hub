from django.core.mail import send_mail
from django.conf import settings

def send_notification_email(subject, message, recipient_list, html_message=None):
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            html_message=html_message  # Optional: if sending HTML email
        )
        return True
    except Exception as e:
        print("Email send failed:", e)
        return False
