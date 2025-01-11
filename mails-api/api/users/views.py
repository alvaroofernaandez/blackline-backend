from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .models import User
from django.core.mail import send_mail
from .UserSerializer import UserSerializer
from .utils import send_email_users_where_allowed

class SendSingleEmailAPIView(APIView):
    def post(self, request):
        correo = request.data.get("correo")
        asunto = request.data.get("asunto")
        mensaje = request.data.get("mensaje")

        if not correo or not asunto or not mensaje:
            return Response(
                {"error": "Por favor, proporciona correo, asunto y mensaje."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            if not User.objects.filter(email=correo).exists():
                return Response(
                    {"error": f"No existe un usuario registrado con el correo: {correo}"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            send_mail(
                subject=asunto,
                message=mensaje,
                from_email="jdeomoya@gmail.com",
                recipient_list=[correo],
                fail_silently=False,
            )

            return Response({"message": "Correo enviado exitosamente!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Error al enviar el correo: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
class SendEmailsAPIView(APIView):
    def post(self, request):
        # Recibir los datos desde el cuerpo de la solicitud.
        asunto = request.data.get("asunto")
        mensaje = request.data.get("mensaje")

        # Validar que los campos sean proporcionados
        if not asunto or not mensaje:
            return Response(
                {"error": "Por favor, proporciona un asunto y un mensaje."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            usuarios = User.objects.filter(can_receive_emails=True)

            if not usuarios.exists():
                return Response(
                    {"error": "No hay usuarios que puedan recibir correos."},
                    status=status.HTTP_404_NOT_FOUND
                )

            correos_destinatarios = usuarios.values_list('email', flat=True)

            send_mail(
                subject=asunto,
                message=mensaje,
                from_email="jdeomoya@gmail.com",
                recipient_list=correos_destinatarios,
                fail_silently=False,
            )

            return Response({"message": "Correos enviados exitosamente!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Error al enviar los correos: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )



class UserCreateAPIView(APIView):
    def getUserById(self,request):
        id_alumno = request.query_params.get('id')

        if not id_alumno:
            return Response({"error": "id_alumno es requerido"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(id=id_alumno).first

        serializer = UserSerializer(user,many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Usuario creado exitosamente!", "user": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)