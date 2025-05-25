from django.core.mail import send_mail

from ..models import User


def send_email_users_where_allowed():
    users = User.objects.filter(can_receive_emails=True)

    if not users.exists():
        raise ValueError("No hay usuarios permitidos para enviar correos.")
    emails = [user.email for user in users]
    send_mail(
        subject="Notificación importante",
        message="Este es un correo enviado a usuarios permitidos.",
        from_email="jdeomoya@gmail.com",
        recipient_list=emails,
    )


