from django.core.mail import send_mail
from .models import User


def send_email_users_where_allowed():
    # Filtrar usuarios que tienen permitido recibir correos
    users = User.objects.filter(can_receive_emails=True)

    if not users.exists():
        raise ValueError("No hay usuarios permitidos para enviar correos.")

    # Enviar correo a todos los usuarios permitidos
    for user in users:
        send_mail(
            subject="Notificación importante",
            message="Este es un correo enviado a usuarios permitidos.",
            from_email="tu_email@gmail.com",  # Cambia esto por tu dirección de correo
            recipient_list=[user.email],
        )