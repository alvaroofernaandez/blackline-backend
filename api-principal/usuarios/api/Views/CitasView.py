import logging
from django.core.exceptions import ValidationError
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..Models.CitaModel import Cita
from ..Serializers.CitaSerializer import CitaSerializer

logger = logging.getLogger('api')

class CitasViewSet(viewsets.ViewSet):
    def list(self, request):
        logger.info("Listando todas las citas")
        citas = Cita.objects.all()
        serializer = CitaSerializer(citas, many=True)
        logger.debug(f"{len(citas)} citas encontradas")
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        logger.info(f"Recuperando cita con id {pk}")
        try:
            cita = Cita.objects.get(pk=pk)
            serializer = CitaSerializer(cita)
            logger.debug(f"Cita encontrada: {serializer.data}")
            return Response(serializer.data)
        except Cita.DoesNotExist:
            logger.warning(f"Cita con id {pk} no encontrada")
            return Response({"error": "Cita no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        logger.info("Creando nueva cita")
        serializer = CitaSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                logger.info("Cita creada correctamente")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                logger.error(f"Error de validación al crear cita: {str(e)}")
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        logger.warning(f"Datos inválidos para crear cita: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        logger.info(f"Actualizando cita con id {pk}")
        try:
            cita = Cita.objects.get(pk=pk)
            serializer = CitaSerializer(cita, data=request.data)
            if serializer.is_valid():
                try:
                    serializer.save()
                    logger.info(f"Cita con id {pk} actualizada correctamente")
                    return Response(serializer.data)
                except ValidationError as e:
                    logger.error(f"Error de validación al actualizar cita: {str(e)}")
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            logger.warning(f"Datos inválidos para actualizar cita: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Cita.DoesNotExist:
            logger.warning(f"Cita con id {pk} no encontrada para actualizar")
            return Response({"error": "Cita no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        logger.info(f"Eliminando cita con id {pk}")
        try:
            cita = Cita.objects.get(pk=pk)
            cita.delete()
            logger.info(f"Cita con id {pk} eliminada correctamente")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Cita.DoesNotExist:
            logger.warning(f"Cita con id {pk} no encontrada para eliminar")
            return Response({"error": "Cita no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], url_path='tramo_horario')
    def get_tramo_horario(self, request):
        fecha = request.query_params.get('fecha')
        logger.info(f"Consultando tramos horarios para la fecha {fecha}")
        if not fecha:
            logger.error("Falta el parámetro 'fecha' en la consulta de tramos horarios")
            return Response({"error": "Se requiere el parámetro 'fecha'"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            citas = Cita.objects.filter(fecha=fecha)
            tramos_disponibles = {
                "1": True,
                "2": True,
                "3": True,
                "4": True,
            }

            for cita in citas:
                if cita.hora in tramos_disponibles:
                    tramos_disponibles[cita.hora] = False

            logger.debug(f"Tramos disponibles para {fecha}: {tramos_disponibles}")
            return Response(tramos_disponibles, status=status.HTTP_200_OK)
        except ValidationError as e:
            logger.error(f"Error de validación al consultar tramos horarios: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
