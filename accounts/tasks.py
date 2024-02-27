from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def send_confirmation_email(user_id, message):
    '''
    Task to send email confirmation link when an account is created.
    '''
    user = User.objects.get(pk=user_id)
    subject = 'Activate your account'

    mail_sent = send_mail(
        subject=subject,
        message=message,
        from_email='admin@shopily.com',
        recipient_list=[user.email],
        fail_silently=False
    )

    return mail_sent
