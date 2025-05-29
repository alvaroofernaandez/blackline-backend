from rest_framework import serializers
from ..Models.DiseñoModel import Design

class DiseñoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Design
        fields = '__all__'

    def update(self, instance, validated_data):
        imagen_file = validated_data.pop('imagen', None)

        if imagen_file:
            instance.imagen = imagen_file  

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
