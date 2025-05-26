from api.Auth.tokens import CustomToken
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import logging

User = get_user_model()
logger = logging.getLogger('api')

class CustomTokenObtainView(APIView):
    def post(self, request):
        logger.info(f"Intento de autenticación para el email: {request.data.get('email')}")
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
            logger.debug(f"Usuario encontrado para el email: {email}")
        except User.DoesNotExist:
            logger.warning(f"Intento fallido de autenticación, usuario no encontrado: {email}")
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            logger.warning(f"Contraseña incorrecta para el usuario: {email}")
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = CustomToken.for_user(user)
        logger.info(f"Autenticación exitosa para el usuario: {email}")
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
