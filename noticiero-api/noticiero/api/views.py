from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Noticias
from .serializers import NoticiasSerializer
from .permissions import IsAdminUser, IsNormalUser

class NoticiasListCreateView(APIView):
    '''
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsNormalUser()]
        elif self.request.method == 'POST':
            return [IsNormalUser()]
        return []
    '''

    def get(self, request):
        noticias = Noticias.objects.all()
        serializer = NoticiasSerializer(noticias, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NoticiasSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NoticiasDetailView(APIView):
    '''
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsNormalUser()]
        elif self.request.method in ['PUT', 'DELETE']:
            return [IsNormalUser()]
        return []
    '''

    def get(self, request, pk):
        try:
            noticia = Noticias.objects.get(id=pk)
        except Noticias.DoesNotExist:
            return Response({"error": "Noticia no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        serializer = NoticiasSerializer(noticia)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            noticia = Noticias.objects.get(id=pk)
        except Noticias.DoesNotExist:
            return Response({"error": "Noticia no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        serializer = NoticiasSerializer(noticia, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            noticia = Noticias.objects.get(id=pk)
        except Noticias.DoesNotExist:
            return Response({"error": "Noticia no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        noticia.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
