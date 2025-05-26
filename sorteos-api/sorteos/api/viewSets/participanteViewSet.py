import logging
import mongoengine
from bson import ObjectId
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models.participanteModel import Participante
from ..models.sorteoModel import Sorteo
from ..serializers.participanteSerializer import ParticipanteSerializer

logger = logging.getLogger("api")

class ParticipanteViewSet(viewsets.ViewSet):

    def _get_sorteo_or_404(self, sorteo_id):
        logger.debug(f"Buscando sorteo con id: {sorteo_id}")
        try:
            sorteo = Sorteo.objects.get(id=ObjectId(sorteo_id))
            logger.info(f"Sorteo encontrado: {sorteo_id}")
            return sorteo
        except (mongoengine.DoesNotExist, mongoengine.ValidationError):
            logger.warning(f"Sorteo no encontrado: {sorteo_id}")
            return None

    @action(detail=True, methods=["post"], url_path="registrar")
    def registrar_participantes(self, request, pk=None):
        logger.info(f"Solicitud para registrar participantes en sorteo {pk}")
        sorteo = self._get_sorteo_or_404(pk)
        if not sorteo:
            logger.error(f"Sorteo no encontrado al registrar participantes: {pk}")
            return Response({"error": "Sorteo no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        multiple = isinstance(data, list)
        serializer = ParticipanteSerializer(data=data, many=multiple)

        if not serializer.is_valid():
            logger.error(f"Datos inválidos al registrar participantes: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        participantes_data = serializer.validated_data
        nuevos_participantes = []

        for participante_data in participantes_data if multiple else [participantes_data]:
            participante = Participante(**participante_data)
            nuevos_participantes.append(participante)
            logger.debug(f"Participante preparado para añadir: {participante_data}")

        sorteo.participantes.extend(nuevos_participantes)
        sorteo.save()
        logger.info(f"{len(nuevos_participantes)} participante(s) añadidos al sorteo {pk}")

        return Response({
            "message": f"{len(nuevos_participantes)} participante(s) añadidos correctamente",
            "total_participantes": len(sorteo.participantes)
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        logger.info(f"Solicitud para obtener participantes del sorteo {pk}")
        sorteo = self._get_sorteo_or_404(pk)
        if not sorteo:
            logger.error(f"Sorteo no encontrado al obtener participantes: {pk}")
            return Response({"error": "Sorteo no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ParticipanteSerializer(sorteo.participantes, many=True)
        logger.debug(f"Participantes serializados para sorteo {pk}")
        return Response(serializer.data, status=status.HTTP_200_OK)
