from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from ..Auth.tokens import CustomToken
from ..models import User

class CustomTokenObtainView(APIView):
    def post(self, request):
        # Comprobamos los datos de el usuario ¡
        password = request.data.get('password')
        email = request.data.get('email')

        try:
            # Filtramos por los usuarios que cumplan con la condicion
            user = User.objects.get(email=email, password=password)

        except User.DoesNotExist:
            # En este caso no había ningun usuario con esas credenciales
            return Response({'error': 'Invalid credentials'}, status=401)


        if user is not None:
            # Generamos el token en funcion de la clase que hemos creado
            refresh = CustomToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })

        else:
            return Response({'error': 'Invalid credentials'}, status=401)
