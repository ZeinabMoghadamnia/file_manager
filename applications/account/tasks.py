from config.celery import app
from django.contrib.auth.tokens import default_token_generator
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse


@app.task
def send_otp_email_task(subject, otp_code, recipient):
    send_mail(subject, f'Your login code is: {otp_code}', settings.EMAIL_HOST_USER, [recipient],
              fail_silently=False)

@app.task
def send_activation_email_task(user_id, activation_url):
    from .models import User
    user = User.objects.get(pk=user_id)
    subject = 'Activate your account'
    message = f'Click the following link to activate your account:\n\n{activation_url}'
    to_email = user.email
    send_mail(subject, message, settings.EMAIL_HOST_USER, [to_email])
