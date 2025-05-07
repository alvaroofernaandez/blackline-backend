from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        # No buscamos en la base de datos, devolvemos solo el payload
        return validated_token
