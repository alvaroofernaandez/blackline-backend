# En tu archivo de vistas
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..Models.DiseñoModel import Design
from ..Serializers.DiseñoSerializer import DiseñoSerializer
from ..permissions import IsNormalUser, IsAdminUser

class DiseñoView(APIView):
    def get(self, request, pk=None, permission_classes=['IsAdminUser']):
        if pk:
            try:
                diseño = Design.objects.get(pk=pk)
                serializer = DiseñoSerializer(diseño)
                return Response(serializer.data)
            except Design.DoesNotExist:
                return Response({"error": "Diseño no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        else:
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

    def put(self, request, pk):
        diseño = Design.objects.get(pk=pk)
        serializer = DiseñoSerializer(diseño, data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        diseño = Design.objects.get(pk=pk)
        try:
            diseño.delete()
            return Response("Diseño eliminado correctamente", status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)