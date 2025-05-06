from rest_framework import viewsets, status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from django.shortcuts import redirect, render, get_object_or_404
from rest_framework.renderers import JSONRenderer
from django.template.loader import render_to_string
from django.http import HttpResponse


from ..Models.FacturaModel import Factura
from ..Serializers.FacturaSerializer import FacturaSerializer
from ..Models.CitaModel import Cita


class FacturaViewSet(viewsets.ModelViewSet):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer

    @action(detail=False, methods=['get'], renderer_classes=[TemplateHTMLRenderer, JSONRenderer])
    def detalle(self, request):
        id = request.query_params.get('id')
        download = request.query_params.get('download') == '1'

        if not id:
            raise ValidationError("Se debe proporcionar un id.")

        factura = get_object_or_404(Factura, pk=id)
        factura_data = FacturaSerializer(factura).data

        if download:
            html_content = render_to_string('factura/factura.html', {'factura': factura_data})
            response = HttpResponse(html_content, content_type='text/html')
            response['Content-Disposition'] = f'attachment; filename=factura_{id}.html'
            return response

        if request.accepted_renderer.format == 'html':
            return Response({'factura': factura_data}, template_name='factura/factura.html')
        else:
            return Response({'factura': factura_data})

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        factura = serializer.save()

        cita = factura.cita
        if cita.estado != 'completada':
            cita.estado = 'completada'
            cita.save()

        return Response({'factura': FacturaSerializer(factura).data}, status=status.HTTP_201_CREATED)
