from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.db import models
from rest_framework import serializers

# Clase Usuarios
class Usuario(models.Model):
    nombre = models.CharField(blank=False, max_length=150)
    apellidos = models.CharField(blank=True,null=True, max_length=250)
    email = models.EmailField(blank=False, unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    #Funcion para validar que los campos email y nombre no estén vacíos
    def clean(self):
        campos = [self.nombre,self.email]
        if any(not c for c in campos):
            raise ValidationError("Los campos nombre y email deben de estar rellenos")

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"