from rest_framework import serializers
from ..Models.DiseñoModel import Design

class DiseñoSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Design
        fields = '__all__'

    def update(self, instance, validated_data):
        imagen_file = validated_data.pop('image', None)

        if imagen_file is not None:
            instance.image = imagen_file

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
