from django.conf import settings
from django.core.mail import EmailMessage


class EmailService:

    @staticmethod
    def send_email(data):
        try:
            email = EmailMessage(
                subject=data.get('email_subject', ''),
                body=data.get('email_body', ''),
                to=[data.get('to_email', '')],
                from_email=settings.EMAIL_HOST_USER
            )
            email.send(fail_silently=False)
        except Exception as e:
            print(e)
            pass
