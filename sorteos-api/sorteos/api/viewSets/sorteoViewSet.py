import logging
import mongoengine as me
from bson import ObjectId
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models.sorteoModel import Sorteo
from ..permissions import IsAdminUser, IsNormalUser, IsViewUser
from ..serializers.sorteoSerializer import SorteoSerializer

logger = logging.getLogger('api')

class SorteoViewSet(viewsets.ViewSet):
    permission_classes = []

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy', 'seleccionar_ganador', 'asignar_premio']:
            logger.info(f'Permisos de administrador requeridos para la acción: {self.action}')
            return [IsAdminUser()]
        logger.info(f'Permisos por defecto para la acción: {self.action}')
        return []

    def get_object(self, sorteo_id):
        try:
            logger.debug(f'Buscando sorteo con id: {sorteo_id}')
            return Sorteo.objects.get(id=ObjectId(sorteo_id))
        except (me.DoesNotExist, me.ValidationError):
            logger.warning(f'Sorteo no encontrado con id: {sorteo_id}')
            return None

    def list(self, request):
        logger.info('Listando todos los sorteos')
        sorteos = Sorteo.objects.all()
        serializer = SorteoSerializer(sorteos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        logger.info(f'Recuperando sorteo con id: {pk}')
        sorteo = self.get_object(pk)
        if not sorteo:
            logger.error(f'Sorteo no encontrado con id: {pk}')
            return Response({"error": "Sorteo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        serializer = SorteoSerializer(sorteo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        logger.info('Creando un nuevo sorteo')
        serializer = SorteoSerializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f'Error de validación al crear sorteo: {serializer.errors}')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            sorteo = Sorteo(**serializer.validated_data)
            sorteo.clean()
            sorteo.save()
            logger.info(f'Sorteo creado correctamente con id: {sorteo.id}')
            return Response({"message": "Sorteo creado correctamente", "id": str(sorteo.id)}, status=status.HTTP_201_CREATED)
        except me.ValidationError as e:
            logger.error(f'Error al crear sorteo: {str(e)}')
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        logger.info(f'Actualizando sorteo con id: {pk}')
        sorteo = self.get_object(pk)
        if not sorteo:
            logger.error(f'Sorteo no encontrado con id: {pk}')
            return Response({"error": "Sorteo no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SorteoSerializer(sorteo, data=request.data, partial=True)
        if not serializer.is_valid():
            logger.error(f'Error de validación al actualizar sorteo: {serializer.errors}')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer.save()
            logger.info(f'Sorteo actualizado correctamente con id: {pk}')
            return Response({"message": "Sorteo actualizado correctamente", "data": serializer.data}, status=status.HTTP_200_OK)
        except me.ValidationError as e:
            logger.error(f'Error al actualizar sorteo: {str(e)}')
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        logger.info(f'Eliminando sorteo con id: {pk}')
        sorteo = self.get_object(pk)
        if not sorteo:
            logger.error(f'Sorteo no encontrado con id: {pk}')
            return Response({"error": "Sorteo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        sorteo.delete()
        logger.info(f'Sorteo eliminado correctamente con id: {pk}')
        return Response({"message": "Sorteo eliminado correctamente"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], url_path='seleccionar_ganador')
    def seleccionar_ganador(self, request, pk=None):
        logger.info(f'Seleccionando ganador para sorteo con id: {pk}')
        sorteo = self.get_object(pk)
        if not sorteo:
            logger.error(f'Sorteo no encontrado con id: {pk}')
            return Response({"error": "Sorteo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        try:
            sorteo.selecGanador()
            sorteo.estado = "finalizado"
            sorteo.save()
            logger.info(f'Ganador seleccionado correctamente para sorteo con id: {pk}')
            return Response({"message": "Ganador seleccionado correctamente", "ganador": str(sorteo.ganador.instagram_username)}, status=status.HTTP_200_OK)
        except ValueError as e:
            logger.error(f'Error al seleccionar ganador: {str(e)}')
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], url_path='asignar_premio')
    def asignar_premio(self, request, pk=None):
        logger.info(f'Asignando premio para sorteo con id: {pk}')
        sorteo = self.get_object(pk)
        if not sorteo:
            logger.error(f'Sorteo no encontrado con id: {pk}')
            return Response({"error": "Sorteo no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        premio = request.data.get("premio")
        if not premio:
            logger.error('No se proporcionó premio para asignar')
            return Response({"error": "Debes asignar un premio"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            sorteo.asignarPremio(premio)
            sorteo.save()
            logger.info(f'Premio asignado correctamente para sorteo con id: {pk}')
            return Response({"message": "Premio asignado correctamente", "premios": sorteo.premios}, status=status.HTTP_200_OK)
        except ValueError as e:
            logger.error(f'Error al asignar premio: {str(e)}')
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
