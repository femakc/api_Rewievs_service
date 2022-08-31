from django.core.mail import send_mail

from users.models import User


def send_mesege(username):
    user = User.objects.get(username=username)
    email = user.email
    subject = 'confirmation_code'
    message = f'{username} ваш конфирмайшен код {user.confirmation_code}'
    return send_mail(subject, message, 'admin@admin.ru', [email])
