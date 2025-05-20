from rest_framework import serializers

from ..Models.CitaModel import Cita
from ..Models.FacturaModel import Factura


class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = ['id', 'cliente', 'cita', 'fecha_emision', 'total']
        read_only_fields = ['fecha_emision', 'total']
