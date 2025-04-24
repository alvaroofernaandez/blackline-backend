from bson import ObjectId
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
import mongoengine as me

from ..models.sorteoModel import Sorteo
from ..serializers.sorteoSerializer import SorteoSerializer

class SorteoViewSet(viewsets.ViewSet):

    def get_object(self, sorteo_id):
        try:
            return Sorteo.objects.get(id=ObjectId(sorteo_id))
        except (me.DoesNotExist, me.ValidationError):
            return None

    def list(self, request):
        sorteos = Sorteo.objects.all()
        serializer = SorteoSerializer(sorteos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        sorteo = self.get_object(pk)
        if not sorteo:
            return Response({"error": "Sorteo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        serializer = SorteoSerializer(sorteo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = SorteoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            sorteo = Sorteo(**serializer.validated_data)
            sorteo.clean()
            sorteo.save()
            return Response({"message": "Sorteo creado correctamente", "id": str(sorteo.id)}, status=status.HTTP_201_CREATED)
        except me.ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        sorteo = self.get_object(pk)
        if not sorteo:
            return Response({"error": "Sorteo no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        sorteo.estado = request.data.get("estado", sorteo.estado)
        try:
            sorteo.clean()
            sorteo.save()
            return Response({"message": "Sorteo actualizado correctamente"}, status=status.HTTP_200_OK)
        except me.ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        sorteo = self.get_object(pk)
        if not sorteo:
            return Response({"error": "Sorteo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        sorteo.delete()
        return Response({"message": "Sorteo eliminado correctamente"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], url_path='seleccionar_ganador')
    def seleccionar_ganador(self, request, pk=None):
        sorteo = self.get_object(pk)
        if not sorteo:
            return Response({"error": "Sorteo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        try:
            sorteo.selecGanador()
            sorteo.estado = "finalizado"
            sorteo.save()
            return Response({"message": "Ganador seleccionado correctamente", "ganador": str(sorteo.ganador.instagram_username)}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], url_path='asignar_premio')
    def asignar_premio(self, request, pk=None):
        sorteo = self.get_object(pk)
        if not sorteo:
            return Response({"error": "Sorteo no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        premio = request.data.get("premio")
        if not premio:
            return Response({"error": "Debes asignar un premio"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            sorteo.asignarPremio(premio)
            sorteo.save()
            return Response({"message": "Premio asignado correctamente", "premios": sorteo.premios}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
