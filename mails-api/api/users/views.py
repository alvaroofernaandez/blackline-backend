from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .models import User
from .UserSerializer import UserSerializer
from .utils import send_email_users_where_allowed

class SendEmailsAPIView(APIView):
    def post(self, request):
        try:
            send_email_users_where_allowed()  # Llama a la función para enviar correos
            return Response({"message": "Correos enviados exitosamente."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserCreateAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Usuario creado exitosamente!", "user": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)