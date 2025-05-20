from django.core.exceptions import ValidationError
from django.db import models


class Design(models.Model):
    image = models.URLField(blank=False)
    titulo = models.CharField(blank=False, max_length=150)
    descripcion = models.CharField(blank=False, max_length=500)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    alto = models.IntegerField(null=False, blank=False)
    ancho = models.IntegerField(null=False, blank=False)
    duracion = models.IntegerField(null=True, blank=True)


    def clean(self):
        if self.precio < 0:
            raise ValidationError("El precio estimado no puede ser negativo.")