from django.core.exceptions import ValidationError
from rest_framework import serializers

from ..models import User


class UsuarioSerializer(serializers.ModelSerializer):

    def comprobarEmail(self, value):
        # Validamos que el email tenga un formato correcto
        if '@' not in value:
            raise ValidationError("El campo email no tiene el formato correcto")
        return value

    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise ValidationError("El email ya existe. Pruebe con otro.")

        data['email'] = self.comprobarEmail(data['email'])

        return data

    class Meta:
        model = User
        fields = '__all__'
