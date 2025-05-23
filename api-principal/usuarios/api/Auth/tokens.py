from rest_framework_simplejwt.tokens import RefreshToken

class CustomToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        token['id'] = str(user.id)
        token['username'] = user.username
        token['email'] = user.email
        token['role'] = user.role

        return token