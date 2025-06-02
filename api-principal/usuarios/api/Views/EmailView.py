import logging
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from ..models import User
from ..Serializers.UserSerializer import UsuarioSerializer
from .utils import send_email_users_where_allowed

logger = logging.getLogger('api')

class SendSingleEmailAPIView(APIView):
    def post(self, request):
        correo = request.data.get("correo")
        asunto = request.data.get("asunto")
        mensaje = request.data.get("mensaje")
        nombre = request.data.get("nombre")

        logger.info(f"Solicitud para enviar correo a un usuario: {correo}")

        if not correo or not asunto or not mensaje or not nombre:
            logger.warning("Faltan datos requeridos para enviar el correo")
            return Response(
                {"error": "Por favor, proporciona correo, asunto, mensaje y nombre."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            if not User.objects.filter(email=correo).exists():
                logger.warning(f"No existe usuario con el correo: {correo}")
                return Response(
                    {"error": f"No existe un usuario registrado con el correo: {correo}"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            email_body = render_to_string('mail/mail.html', {'nombre': nombre, 'mensaje': mensaje, 'asunto': asunto})

            send_mail(
                subject=asunto,
                message=mensaje,
                from_email="blacklineblackline2@gmail.com",
                recipient_list=[correo],
                fail_silently=False,
                html_message=email_body
            )

            logger.info(f"Correo enviado exitosamente a {correo}")
            return Response({"message": "Correo enviado exitosamente!"}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error al enviar el correo a {correo}: {str(e)}")
            return Response(
                {"error": f"Error al enviar el correo: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class SendEmailsAPIView(APIView):
    def post(self, request):
        asunto = request.data.get("asunto")
        mensaje = request.data.get("mensaje")

        logger.info("Solicitud para enviar correos a todos los usuarios permitidos")

        if not asunto or not mensaje:
            logger.warning("Faltan asunto o mensaje para el envío masivo")
            return Response(
                {"error": "Por favor, proporciona un asunto y un mensaje."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            usuarios = User.objects.filter(can_receive_emails=True)

            if not usuarios.exists():
                logger.warning("No hay usuarios que puedan recibir correos")
                return Response(
                    {"error": "No hay usuarios que puedan recibir correos."},
                    status=status.HTTP_404_NOT_FOUND
                )

            correos_destinatarios = usuarios.values_list('email', flat=True)

            html_message = render_to_string('mail/mail.html', { 'mensaje': mensaje, 'asunto': asunto})

            for correo in correos_destinatarios:
                send_mail(
                    subject=asunto,
                    message=mensaje,
                    from_email="blacklineblackline2@gmail.com",
                    recipient_list=[correo],
                    html_message=html_message,
                    fail_silently=False,
                )
                logger.info(f"Correo enviado a {correo}")

            logger.info("Correos enviados exitosamente a todos los usuarios permitidos")
            return Response({"message": "Correos enviados exitosamente!"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error al enviar los correos: {str(e)}")
            return Response(
                {"error": f"Error al enviar los correos: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=['POST'])
    def send_personalized_email(self, request):
        nombre = request.data.get("nombre")
        correo = request.data.get("correo")
        asunto = request.data.get("asunto")
        mensaje = request.data.get("mensaje")

        logger.info(f"Solicitud para enviar correo personalizado a {correo}")

        if not nombre or not correo or not asunto or not mensaje:
            logger.warning("Faltan datos para el correo personalizado")
            return Response("Error: Inserte nombre, correo, asunto y mensaje.", status=status.HTTP_400_BAD_REQUEST)

        try:
            if not User.objects.filter(email=correo).exists():
                logger.warning(f"No existe usuario con el correo: {correo}")
                return Response(
                    {"error": f"No existe un usuario registrado con el correo: {correo}"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            email_body = render_to_string('mail/mail.html', {'nombre': nombre, 'mensaje': mensaje, 'asunto': asunto})

            send_mail(
                subject=asunto,
                message=mensaje,
                from_email="blacklineblackline2@gmail.com",
                recipient_list=[correo],
                fail_silently=False,
                html_message=email_body
            )

            logger.info(f"Correo personalizado enviado a {correo}")
            return Response({"message": "Correo enviado exitosamente!"}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error al enviar el correo personalizado a {correo}: {str(e)}")
            return Response(
                {"error": f"Error al enviar el correo: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=['POST'])
    def send_personalized_email_many_users(self, request):
        usuarios = request.data.get("usuarios")
        asunto = request.data.get("asunto")
        mensaje = request.data.get("mensaje")

        logger.info("Solicitud para enviar correos personalizados a varios usuarios")

        if not usuarios or not isinstance(usuarios,list) or not asunto or not mensaje:
            logger.warning("Datos inválidos para el envío a múltiples usuarios")
            return Response(
                {"error": "Debes proporcionar una lista de usuarios, un asunto y un mensaje."},
                status=status.HTTP_400_BAD_REQUEST
            )

        correos_validos = []
        correos_no_encontrado = []

        for correo in usuarios:
            if User.objects.filter(email=correo).exists():
                correos_validos.append(correo)
            else:
                correos_no_encontrado.append(correo)

        if not correos_validos:
            logger.warning("Ningún correo proporcionado existe en la base de datos")
            return Response(
                {"error": "Ninguno de los correos proporcionados existe en la base de datos."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            send_mail(
                subject=asunto,
                message=mensaje,
                from_email="blacklineblackline2@gmail.com",
                recipient_list=correos_validos,
                fail_silently=False,
            )
            logger.info(f"Correos enviados a: {correos_validos}")
            respuesta = {
                "mensaje": "Correos enviados exitosamente.",
                "correos_enviados": correos_validos,
            }
            if correos_no_encontrado:
                logger.warning(f"Correos no encontrados: {correos_no_encontrado}")
                respuesta["correos_no_encontrados"] = correos_no_encontrado

            return Response(respuesta, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error al enviar correos a múltiples usuarios: {str(e)}")
            return Response(
                {"error": f"Error al enviar correos: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class SendEmailWhenPasswordResetAPIView(APIView):
    def post(self, request):
        correo = request.data.get("correo")

        logger.info(f"Solicitud para enviar correo de reseteo de contraseña a {correo}")

        if not correo:
            logger.warning("No se proporcionó correo para el reseteo de contraseña")
            return Response(
                {"error": "Por favor, proporciona un correo."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            usuario = User.objects.get(email=correo)
        except User.DoesNotExist:
            logger.warning(f"El correo proporcionado no existe: {correo}")
            return Response(
                {"error": "El correo proporcionado no existe."},
                status=status.HTTP_400_BAD_REQUEST
            )

        token = RefreshToken.for_user(usuario)
        token['id'] = str(usuario.id)
        token['username'] = usuario.username
        token['email'] = usuario.email
        token['role'] = usuario.role

        reset_url = f"https://blackline-tattoo.hagalink.es/cambiar_contrasena/?token={str(token.access_token)}"

        asunto = "Cambio de contraseña"
        mensaje = f"Para cambiar tu contraseña, haz clic en el siguiente enlace:\n{reset_url}"

        try:
            send_mail(
                subject=asunto,
                message=mensaje,
                from_email="blacklineblackline2@gmail.com",
                recipient_list=[correo],
                fail_silently=False,
            )
            logger.info(f"Correo de reseteo de contraseña enviado a {correo}")
            respuesta = {
                "mensaje": "Correo enviado exitosamente.",
                "correo_persona": correo,
            }

            return Response(respuesta, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error al enviar el correo de reseteo de contraseña a {correo}: {str(e)}")
            return Response(
                {"error": f"Error al enviar el correo: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserCreateAPIView(APIView):
    def getUserById(self,request):
        id_alumno = request.query_params.get('id')

        logger.info(f"Solicitud para obtener usuario por id: {id_alumno}")

        if not id_alumno:
            logger.warning("id_alumno es requerido")
            return Response({"error": "id_alumno es requerido"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(id=id_alumno).first

        serializer = UsuarioSerializer(user,many=False)

        logger.info(f"Usuario obtenido: {serializer.data}")

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        logger.info("Solicitud para obtener todos los usuarios")
        users = User.objects.all()
        serializer = UsuarioSerializer(users, many=True)
        logger.info(f"Usuarios obtenidos: {len(users)}")
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self, request):
        logger.info("Solicitud para crear un nuevo usuario")
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            logger.info(f"Usuario creado exitosamente: {serializer.data}")
            return Response({"message": "Usuario creado exitosamente!", "user": serializer.data}, status=status.HTTP_201_CREATED)
        logger.warning(f"Error al crear usuario: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
