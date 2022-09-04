from django.core.mail import send_mail

from users.models import User
from api_yamdb.settings import DEFAULT_FROM_EMAIL


def send_message(username):
    user = User.objects.get(username=username)
    email = user.email
    subject = 'confirmation_code'
    message = f'{username} ваш конфирмайшен код {user.confirmation_code}'
    return send_mail(subject, message, DEFAULT_FROM_EMAIL, [email])
