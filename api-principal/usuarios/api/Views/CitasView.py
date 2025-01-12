from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..Models.CitaModel import Cita
from ..Serializers.CitaSerializer import CitaSerializer

class CitasViewSet(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                citas = Cita.objects.get(pk=pk)
                serializer = CitaSerializer(citas)
                return Response(serializer.data)
            except Cita.DoesNotExist:
                return Response({"error": "Diseño no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        else:
            citas = Cita.objects.all()
            serializer = CitaSerializer(citas, many=True)
            return Response(serializer.data)