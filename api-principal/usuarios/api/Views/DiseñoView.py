# En tu archivo de vistas
from rest_framework import status, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from ..Models.DiseñoModel import Design
from ..permissions import IsAdminUser, IsNormalUser
from ..Serializers.DiseñoSerializer import DiseñoSerializer


class DiseñoView(viewsets.ModelViewSet):
    queryset = Design.objects.all()
    serializer_class = DiseñoSerializer
#    permission_classes = [IsNormalUser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            instance.delete()
            return Response("Diseño eliminado correctamente", status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)