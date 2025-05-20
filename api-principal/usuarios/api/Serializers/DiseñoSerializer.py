from rest_framework import serializers

from ..Models.DiseñoModel import Design


class DiseñoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Design
        fields = '__all__'
