from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..Models.CitaModel import Cita
from ..Serializers.CitaSerializer import CitaSerializer
from django.core.exceptions import ValidationError

class CitasViewSet(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                cita = Cita.objects.get(pk=pk)
                serializer = CitaSerializer(cita)
                return Response(serializer.data)
            except Cita.DoesNotExist:
                return Response({"error": "Cita no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        else:
            citas = Cita.objects.all()
            serializer = CitaSerializer(citas, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = CitaSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if pk:
            try:
                cita = Cita.objects.get(pk=pk)
                serializer = CitaSerializer(cita, data=request.data)
                if serializer.is_valid():
                    try:
                        serializer.save()
                        return Response(serializer.data)
                    except ValidationError as e:
                        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Cita.DoesNotExist:
                return Response({"error": "Cita no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Se requiere el id de la cita"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if pk:
            try:
                cita = Cita.objects.get(pk=pk)
                cita.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Cita.DoesNotExist:
                return Response({"error": "Cita no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Se requiere el id de la cita"}, status=status.HTTP_400_BAD_REQUEST)
    
    def get_tramo_horario(self, request):
        #Obtener los tramos disponibles del dia seleccionado
        fecha = request.query_params.get('fecha')
        if not fecha:
            return Response({"error": "Se requiere el parámetro 'fecha'"}, status=status.HTTP_400_BAD_REQUEST)
        
        try: 
            citas = Cita.objects.filter(fecha=fecha)
            tramos_disponibles = {
                "09:00-11:00": True,
                "11:00-13:00": True,
                "15:00-17:00": True,
                "17:00-19:00": True,
            }
            
            for cita in citas:
                if cita.hora in tramos_disponibles:
                    tramos_disponibles[cita.hora] = False
            
            return Response(tramos_disponibles, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)     