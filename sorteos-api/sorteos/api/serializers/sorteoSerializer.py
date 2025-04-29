from rest_framework import serializers
from ..models.sorteoModel import ESTADOS_SORTEOS
from .participanteSerializer import ParticipanteSerializer

class SorteoSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    titulo = serializers.CharField(max_length=255)
    descripcion = serializers.CharField(allow_blank=True, required=False)
    fecha_inicio = serializers.DateTimeField()
    fecha_fin = serializers.DateTimeField()
    estado = serializers.ChoiceField(choices=ESTADOS_SORTEOS, default="activo")
    ganador = serializers.SerializerMethodField()
    premios = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    participantes = ParticipanteSerializer(many=True, read_only=True)

    def get_ganador(self, sorteo):
        return str(sorteo.ganador.instagram_username) if sorteo.ganador else None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["ganador"] = self.get_ganador(instance)
        return representation

    def validate(self, data):
        if data['fecha_inicio'] >= data['fecha_fin']:
            raise serializers.ValidationError("La fecha de inicio debe ser anterior a la fecha de fin.")
        return data
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
