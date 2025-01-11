from rest_framework import serializers
from ..Models.UserModel import Usuario
from django.core.exceptions import ValidationError


class UsuarioSerializer(serializers.ModelSerializer):

    def comprobarEmail(self, value):
        # Validamos que el email tenga un formato correcto
        if '@' not in value:
            raise ValidationError("El campo email no tiene el formato correcto")
        return value

    def validate(self, data):
        if Usuario.objects.filter(email=data['email']).exists():
            raise ValidationError("El email ya existe. Pruebe con otro.")

        data['email'] = self.comprobarEmail(data['email'])

        return data

    class Meta:
        model = Usuario
        fields = '__all__'
