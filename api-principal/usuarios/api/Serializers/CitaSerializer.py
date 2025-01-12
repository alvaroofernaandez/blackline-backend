from rest_framework import serializers
from ..Models.CitaModel import Cita

class CitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cita
        fields = '__all__'
