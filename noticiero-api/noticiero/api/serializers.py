from rest_framework import serializers

from .models import Noticias

class NoticiasSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    titulo = serializers.CharField()
    descripcion = serializers.CharField(allow_blank=True, required=False)
    imagen = serializers.CharField(allow_blank=True, required=False)
    fecha = serializers.DateTimeField()

    def create(self, validated_data):
        return Noticias(**validated_data).save()

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
