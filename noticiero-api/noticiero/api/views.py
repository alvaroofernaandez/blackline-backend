import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.http import Http404

from .models import Noticias
from .serializers import NoticiasSerializer
from .permissions import IsAdminUser, IsNormalUser

logger = logging.getLogger('api')

class NoticiasListCreateAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        return [IsAdminUser()]

    def get(self, request):

        logger.info("Solicitud GET recibida para listar noticias")
        noticias = Noticias.objects()
        serializer = NoticiasSerializer(noticias, many=True, context={'request': request})
        logger.debug(f"{len(serializer.data)} noticias encontradas")
        return Response(serializer.data)

    def post(self, request):
        logger.info("Solicitud POST recibida para crear noticia")
        logger.debug(f"Datos recibidos: {request.data}")
        logger.debug(f"Archivos recibidos: {request.FILES}")
        
        serializer = NoticiasSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            logger.info("Noticia creada exitosamente")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        logger.warning(f"Error al crear noticia: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NoticiasDetailAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        return [IsAdminUser()]

    def get_object(self, id):
        try:
            logger.debug(f"Buscando noticia con id {id}")
            return Noticias.objects.get(id=id)
        except Noticias.DoesNotExist:
            logger.error(f"No se encontró la noticia con id {id}")
            raise Http404

    def get(self, request, id):
        logger.info(f"Solicitud GET recibida para noticia con id {id}")
        noticia = self.get_object(id)
        serializer = NoticiasSerializer(noticia, context={'request': request})
        return Response(serializer.data)

    def put(self, request, id):
        logger.info(f"Solicitud PUT recibida para noticia con id {id}")
        logger.debug(f"Datos recibidos: {request.data}")
        logger.debug(f"Archivos recibidos: {request.FILES}")
        
        noticia = self.get_object(id)
        serializer = NoticiasSerializer(noticia, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Noticia con id {id} actualizada exitosamente")
            return Response(serializer.data)
        
        logger.warning(f"Error al actualizar noticia con id {id}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        logger.info(f"Solicitud DELETE recibida para noticia con id {id}")
        noticia = self.get_object(id)
        noticia.delete() 
        logger.info(f"Noticia con id {id} eliminada exitosamente")
        return Response(status=status.HTTP_204_NO_CONTENT)