from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Noticias
from .serializers import NoticiasSerializer
from .permissions import IsAdminUser, IsNormalUser

class NoticiasViewSet(viewsets.ModelViewSet):
    queryset = Noticias.objects.all()
    serializer_class = NoticiasSerializer

    '''
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsNormalUser()]
        elif self.request.method in ['POST', 'PUT', 'DELETE']:
            return [IsNormalUser()]
        return []
    '''
