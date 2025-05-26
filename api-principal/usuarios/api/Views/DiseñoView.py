import logging
from rest_framework import status, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from ..Models.DiseñoModel import Design
from ..permissions import IsAdminUser, IsNormalUser
from ..Serializers.DiseñoSerializer import DiseñoSerializer

logger = logging.getLogger('api')

class DiseñoView(viewsets.ModelViewSet):
    queryset = Design.objects.all()
    serializer_class = DiseñoSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def list(self, request, *args, **kwargs):
        logger.info("Listando todos los diseños")
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Recuperando diseño con id {kwargs.get('pk')}")
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info("Creando un nuevo diseño")
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            logger.info("Diseño creado correctamente")
        else:
            logger.warning(f"Error al crear diseño: {response.data}")
        return response

    def update(self, request, *args, **kwargs):
        logger.info(f"Actualizando diseño con id {kwargs.get('pk')}")
        response = super().update(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            logger.info("Diseño actualizado correctamente")
        else:
            logger.warning(f"Error al actualizar diseño: {response.data}")
        return response

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        logger.info(f"Eliminando diseño con id {instance.id}")
        try:
            instance.delete()
            logger.info("Diseño eliminado correctamente")
            return Response("Diseño eliminado correctamente", status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f"Error al eliminar diseño: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)