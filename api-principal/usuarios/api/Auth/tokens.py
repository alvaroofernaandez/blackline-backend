from rest_framework_simplejwt.tokens import RefreshToken


# Método personalizado para devolver un token con el id, username, email y rol del usuario
class CustomToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)

        # Añadimos información adicional al token
        token['id'] = str(user.id)
        token['username'] = user.username
        token['email'] = user.email
        token['role'] = user.role
        token['instagram_username'] = user.instagram_username
        token['can_receive_emails'] = user.can_receive_emails

        return token