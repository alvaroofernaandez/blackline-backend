import logging
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from weasyprint import HTML

from ..Models.CitaModel import Cita
from ..Models.FacturaModel import Factura
from ..Serializers.FacturaSerializer import FacturaSerializer

logger = logging.getLogger('api')

class FacturaViewSet(viewsets.ModelViewSet):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer

    @action(detail=False, methods=['get'], renderer_classes=[TemplateHTMLRenderer, JSONRenderer])
    def detalle(self, request):
        id = request.query_params.get('id')
        download = request.query_params.get('download') == '1'

        logger.info(f'Solicitud de detalle de factura recibida. id={id}, download={download}')

        if not id:
            logger.warning('No se proporcionó id en la solicitud de detalle de factura.')
            raise ValidationError("Se debe proporcionar un id.")

        factura = get_object_or_404(Factura, pk=id)
        logger.debug(f'Factura encontrada: {factura.pk}')

        if download:
            logger.info(f'Generando PDF para la factura {id}')
            html_content = render_to_string('factura/factura.html', {'factura': factura})
            pdf_file = HTML(string=html_content).write_pdf()
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename=factura_{id}.pdf'
            logger.info(f'PDF generado y enviado para la factura {id}')
            return response

        if request.accepted_renderer.format == 'html':
            logger.info(f'Respondiendo con HTML para la factura {id}')
            return Response({'factura': factura}, template_name='factura/factura.html')
        else:
            logger.info(f'Respondiendo con JSON para la factura {id}')
            factura_data = FacturaSerializer(factura).data
            return Response({'factura': factura_data})
    def create(self, request):
        logger.info('Solicitud de creación de factura recibida.')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        factura = serializer.save()
        logger.info(f'Factura creada con id {factura.pk}')

        cita = factura.cita
        if cita.estado != 'completada':
            logger.info(f'Actualizando estado de la cita {cita.pk} a completada')
            cita.estado = 'completada'
            cita.save()

        logger.info(f'Respuesta de creación de factura enviada para la factura {factura.pk}')
        return Response({'factura': FacturaSerializer(factura).data}, status=status.HTTP_201_CREATED)
