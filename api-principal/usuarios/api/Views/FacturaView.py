from rest_framework import viewsets, status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from django.shortcuts import redirect, render, get_object_or_404

from ..Models.FacturaModel import Factura
from ..Serializers.FacturaSerializer import FacturaSerializer
from ..Models.CitaModel import Cita


class FacturaViewSet(viewsets.ModelViewSet):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer


    @action(detail=False,methods=['get'], renderer_classes=[TemplateHTMLRenderer])
    def detalle(self, request):
        id = request.data.get('id')

        if not id:
            raise ValidationError("Se debe proporcionar un id.")

        factura = get_object_or_404(Factura, pk=id)
        return Response({'factura': factura}, template_name='factura/detalle.html')

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        factura = serializer.save()

        total = 0

        for cita in factura.citas.all():
            if cita.estado != 'completada':
                cita.estado = 'completada'
                cita.save()


        factura.total = total
        factura.save()

        return Response({'factura': serializer.data}, status=status.HTTP_201_CREATED)

