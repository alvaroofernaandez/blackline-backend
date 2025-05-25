from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from ..models import User
from ..Serializers.UserSerializer import UsuarioSerializer
from ..permissions import IsAdminUser, IsNormalUser


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer

    # Método para añadir un usuario
    @action(detail=False, methods=['post'], url_path='registrar_user', name='registrar_user')
    def registrar_user(self, request):
        contenido = {
            'username': str(request.data.get('username', '')).strip(),
            'email': str(request.data.get('email', '')).strip(),
            'password': str(request.data.get('password', '')).strip(),
            'can_receive_emails': str(request.data.get('can_receive_emails', 'false')).lower() == 'true'
        }

        for key in ['email', 'password', 'can_receive_emails']:
            if key not in request.data or request.data[key] in [None, '']:
                return Response(
                    {"error": f"El campo '{key}' es obligatorio."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        try:
            EmailValidator()(contenido['email'])
        except ValidationError:
            return Response(
                {"error": "El campo 'email' no tiene el formato correcto."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(email=contenido['email']).exists():
            return Response(
                {"error": "El email ya existe. Pruebe con otro."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            usuario = User(
                username=contenido['username'],
                email=contenido['email'],
                can_receive_emails=contenido['can_receive_emails']
            )
            usuario.set_password(contenido['password'])
            usuario.save()

            return Response(
                {"mensaje": f"El usuario con el id {usuario.pk} ha sido añadido correctamente"},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"error": f"Error al crear el usuario: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['patch'], url_path='modificar-instagram-username')
    def modificar_instagram_username(self, request):
        user_id = request.data.get('id')
        nuevo_username = request.data.get('instagram_username')

        if not user_id or not nuevo_username:
            return Response(
                {"error": "Los campos 'id' e 'instagram_username' son obligatorios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            if User.objects.filter(instagram_username=nuevo_username).exclude(id=user_id).exists():
                return Response(
                    {"error": "El nombre de usuario de Instagram ya está en uso."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = User.objects.get(id=user_id)
            user.instagram_username = nuevo_username
            user.save()

            return Response(
                {"mensaje": f"Instagram username del usuario {user_id} actualizado correctamente."},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {"error": f"Usuario con id {user_id} no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"No se pudo actualizar el instagram_username: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['patch'], url_path='modificar-recibir-correos')
    def modificar_can_receive_emails(self, request):
        user_id = request.data.get('id')
        nuevo_valor = request.data.get('can_receive_emails')

        if user_id is None or nuevo_valor is None:
            return Response(
                {"error": "Los campos 'id' y 'can_receive_emails' son obligatorios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if isinstance(nuevo_valor, str):
            nuevo_valor = nuevo_valor.strip().lower() == 'true'

        try:
            user = User.objects.get(id=user_id)
            user.can_receive_emails = nuevo_valor
            user.save()
            return Response(
                {"mensaje": f"'can_receive_emails' del usuario {user_id} actualizado a {user.can_receive_emails}"},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {"error": f"Usuario con id {user_id} no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"No se pudo actualizar: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )


    @action(detail=False, methods=['put'], permission_classes=[IsAdminUser])
    def modificar_User(self,request):
        id_usuario = request.data.get('id_usuario')

        if not id_usuario:
            return Response({"error": f"El campo id_usuario es obligatorio"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            usuario = User.objects.get(id=id_usuario)
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        nombre = request.data.get('nombre')
        apellidos = request.data.get('apellidos')
        email = request.data.get('email')

        if not any([nombre, apellidos, email]):
            return Response(
                {"error": "Debes proporcionar al menos un campo para modificar (nombre, apellidos, o email)"},
                status=status.HTTP_400_BAD_REQUEST)

        if nombre:
            usuario.username = nombre
        if email:
            usuario.email = email

        usuario.save()

        return Response({"mensaje": f"Usuario con id {usuario.id} modificado correctamente"},
                        status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'])
    def modificar_contrasena(self, request):
        nueva_contrasena = request.data.get('nueva_contrasena')
        token_str = request.data.get('token')

        if not nueva_contrasena or not token_str:
            return Response(
                {"error": "Los campos 'nueva_contrasena' y 'token' son obligatorios"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = AccessToken(token_str)
        except Exception:
            return Response({"error": "Token inválido o expirado"}, status=status.HTTP_401_UNAUTHORIZED)

        id_usuario = token['id']

        try:
            usuario = User.objects.get(id=id_usuario)
            usuario.set_password(nueva_contrasena)
            usuario.save()

            return Response(
                {"mensaje": f"Contraseña del usuario con id {id_usuario} modificada correctamente"},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {"error": f"Usuario con id {id_usuario} no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )
    @action(detail=False, methods=['delete'], permission_classes=[IsAdminUser])
    def eliminar_User(self,request):
        id_usuario = request.query_params.get('id_usuario')

        if not id_usuario:
            return Response({"error": f"Introduzca un id"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            usuario = User.objects.get(id=id_usuario)

            usuario.delete()

            return Response({"mensaje": f"El usuario con el id {id_usuario} ha sido correctamente eliminado"},
                            status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": f"El usuario con el id {id_usuario} no existe"},
                            status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], permission_classes=[IsNormalUser])
    def buscar_User(self, request):
        id_usuario = request.query_params.get('id_usuario')

        if not id_usuario:
            return Response({"error": "El campo 'id_usuario' es obligatorio"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            usuario = User.objects.get(id=id_usuario)

            serializer = UsuarioSerializer(usuario)

            return Response({"usuario": serializer.data}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": f"El usuario con el id {id_usuario} no existe"},
                            status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def usuariosAntiguos(self, request):
        limite_usuarios = int(request.query_params.get('limit', 5))

        usuarios = User.objects.all().order_by('fecha_registro')[:limite_usuarios]

        serializer = UsuarioSerializer(usuarios, many=True)

        return Response({"usuarios": serializer.data}, status=status.HTTP_200_OK)