from bson import ObjectId
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models.participanteModel import Participante
from ..models.sorteoModel import Sorteo
from ..serializers.participanteSerializer import ParticipanteSerializer
import mongoengine

class ParticipanteViewSet(viewsets.ViewSet):

    def _get_sorteo_or_404(self, sorteo_id):
        try:
            return Sorteo.objects.get(id=ObjectId(sorteo_id))
        except (mongoengine.DoesNotExist, mongoengine.ValidationError):
            return None

    @action(detail=True, methods=["post"], url_path="registrar")
    def registrar_participantes(self, request, pk=None):
        sorteo = self._get_sorteo_or_404(pk)
        if not sorteo:
            return Response({"error": "Sorteo no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        multiple = isinstance(data, list)
        serializer = ParticipanteSerializer(data=data, many=multiple)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        participantes_data = serializer.validated_data
        nuevos_participantes = []

        for participante_data in participantes_data if multiple else [participantes_data]:
            participante = Participante(**participante_data)
            nuevos_participantes.append(participante)

        sorteo.participantes.extend(nuevos_participantes)
        sorteo.save()

        return Response({
            "message": f"{len(nuevos_participantes)} participante(s) añadidos correctamente",
            "total_participantes": len(sorteo.participantes)
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        sorteo = self._get_sorteo_or_404(pk)
        if not sorteo:
            return Response({"error": "Sorteo no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ParticipanteSerializer(sorteo.participantes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
