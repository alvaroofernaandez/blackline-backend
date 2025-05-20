from django.core.exceptions import ValidationError
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..Models.CitaModel import Cita
from ..Serializers.CitaSerializer import CitaSerializer


class CitasViewSet(viewsets.ViewSet):
    def list(self, request):
        citas = Cita.objects.all()
        serializer = CitaSerializer(citas, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            cita = Cita.objects.get(pk=pk)
            serializer = CitaSerializer(cita)
            return Response(serializer.data)
        except Cita.DoesNotExist:
            return Response({"error": "Cita no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = CitaSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            cita = Cita.objects.get(pk=pk)
            serializer = CitaSerializer(cita, data=request.data)
            if serializer.is_valid():
                try:
                    serializer.save()
                    return Response(serializer.data)
                except ValidationError as e:
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Cita.DoesNotExist:
            return Response({"error": "Cita no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            cita = Cita.objects.get(pk=pk)
            cita.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Cita.DoesNotExist:
            return Response({"error": "Cita no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], url_path='tramo_horario')
    def get_tramo_horario(self, request):
        fecha = request.query_params.get('fecha')
        if not fecha:
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

            return Response(tramos_disponibles, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
