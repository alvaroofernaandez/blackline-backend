# En tu archivo de vistas
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..Models.DiseñoModel import Design
from ..Serializers.DiseñoSerializer import DiseñoSerializer

class DiseñoView(APIView):
    def get(self, request):
        diseño = Design.objects.all()
        serializer = DiseñoSerializer(diseño, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DiseñoSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)