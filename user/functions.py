from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings


def send_confirmation_email(user, token):
    subject = 'Confirm your email'
    encode_token = urlsafe_base64_encode(force_bytes(token))
    message = f'Please click the following link to confirm your email: https://backend.anastasiia-uenal.de/confirm_email/{encode_token}/'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])