from django.contrib.sites import requests
from rest_framework import viewsets, status
from rest_framework.decorators import action
from ..permissions import IsAdminUser, IsNormalUser
from rest_framework.response import Response
from ..models import User
from ..Serializers.UserSerializer import UsuarioSerializer
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer


    # Metodo para añadir un usuario

    @action(detail=False, methods=['post'])
    def registrar_User(self, request):
        contenido = {
            'username': str(request.data.get('username', '')).strip(),
            'email': str(request.data.get('email', '')).strip(),
            'password': str(request.data.get('password', '')).strip(),
            'can_receive_emails': str(request.data.get('can_receive_emails', 'false')).lower() == 'true'
        }

        # Validación más precisa
        for key in ['email', 'password', 'can_receive_emails']:
            if key not in request.data or request.data[key] in [None, '']:
                return Response({"error": f"El campo '{key}' es obligatorio."},
                                status=status.HTTP_400_BAD_REQUEST)

        try:
            EmailValidator()(contenido['email'])
        except ValidationError:
            return Response({"error": "El campo 'email' no tiene el formato correcto."},
                            status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=contenido['email']).exists():
            return Response({"error": "El email ya existe. Pruebe con otro."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            usuario = User(
                username=contenido['username'],
                email=contenido['email'],
                can_receive_emails=contenido['can_receive_emails']
            )
            usuario.set_password(contenido['password'])
            usuario.save()

            return Response({"mensaje": f"El usuario con el id {usuario.pk} ha sido añadido correctamente"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"Error al crear el usuario: {str(e)}"},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['patch'], url_path='modificar-recibir-correos')
    def modificar_can_receive_emails(self, request):
        user = request.user
        nuevo_valor = request.data.get('can_receive_emails')

        if nuevo_valor is None:
            return Response({"error": "El campo 'can_receive_emails' es obligatorio."},
                            status=status.HTTP_400_BAD_REQUEST)

        if isinstance(nuevo_valor, str):
            nuevo_valor = nuevo_valor.strip().lower() == 'true'

        try:
            user.can_receive_emails = nuevo_valor
            user.save()
            return Response({"mensaje": f"'can_receive_emails' actualizado a {user.can_receive_emails}"},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"No se pudo actualizar: {str(e)}"},
                            status=status.HTTP_400_BAD_REQUEST)

    # Metodo para modificar un usuario
    @action(detail=False, methods=['put'], permission_classes=[IsAdminUser])
    def modificar_User(self,request):
        # Campo obligatorioDTO.UserDTO
        # Campo obligatorio
        id_usuario = request.data.get('id_usuario')

        if not id_usuario:
            return Response({"error": f"El campo id_usuario es obligatorio"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Ahora comprobamos que el usuario si existe el usuario en la bbdd
        try:
            usuario = User.objects.get(id=id_usuario)
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # Obtenemos los datos que ha introducido el usuario
        nombre = request.data.get('nombre')
        apellidos = request.data.get('apellidos')
        email = request.data.get('email')

        # Comprobamos que el usuario haya introducido al menos un campo
        if not any([nombre, apellidos, email]):
            return Response(
                {"error": "Debes proporcionar al menos un campo para modificar (nombre, apellidos, o email)"},
                status=status.HTTP_400_BAD_REQUEST)

        # Modifico los campos ha dado el usuario
        if nombre:
            usuario.username = nombre
        if email:
            usuario.email = email

        # Guardamos el usuario en la bbdd
        usuario.save()

        # Devuelvo el mensaje de que todo ha ido bien
        return Response({"mensaje": f"Usuario con id {usuario.id} modificado correctamente"},
                        status=status.HTTP_200_OK)

    # Metodo para eliminar Usuarios
    @action(detail=False, methods=['delete'], permission_classes=[IsAdminUser])
    def eliminar_User(self,request):
        id_usuario = request.query_params.get('id_usuario')

        if not id_usuario:
            return Response({"error": f"Introduzca un id"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # Obtenemos a el usuario
            usuario = User.objects.get(id=id_usuario)

            # Eliminamos a el usuario
            usuario.delete()

            return Response({"mensaje": f"El usuario con el id {id_usuario} ha sido correctamente eliminado"},
                            status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": f"El usuario con el id {id_usuario} no existe"},
                            status=status.HTTP_404_NOT_FOUND)

    # Metodo para buscar un usuario por id
    @action(detail=False, methods=['get'], permission_classes=[IsNormalUser])
    def buscar_User(self, request):
        # Obtenemos el id introducido por el usuario
        id_usuario = request.query_params.get('id_usuario')

        # Comprobamos si ha introducido el id o no
        if not id_usuario:
            return Response({"error": "El campo 'id_usuario' es obligatorio"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # Buscamos a el usuario y devolvemos el json que corresponde a ese usuario
            usuario = User.objects.get(id=id_usuario)

            serializer = UsuarioSerializer(usuario)

            return Response({"usuario": serializer.data}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": f"El usuario con el id {id_usuario} no existe"},
                            status=status.HTTP_404_NOT_FOUND)

    # Método para obtener los usuarios mas antiguos
    @action(detail=False, methods=['get'])
    def usuariosAntiguos(self, request):
        #Obtenemos el limite de usuarios introducido por el usuario
        limite_usuarios = int(request.query_params.get('limit', 5))

        # Filtramos por la fecha de usuarios
        usuarios = User.objects.all().order_by('fecha_registro')[:limite_usuarios]

        # Serializamos los datos
        serializer = UsuarioSerializer(usuarios, many=True)

        # Devolvemos los usuarios por orden de llegada de más antiguo a más reciente
        return Response({"usuarios": serializer.data}, status=status.HTTP_200_OK)