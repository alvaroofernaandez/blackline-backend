from django.core.exceptions import ValidationError
from django.db import models

class Design(models.Model):
    image = models.URLField(blank=False)
    titulo = models.CharField(blank=False, max_length=150)
    descripcion = models.CharField(blank=False, max_length=500)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    alto = models.IntegerField(max_digits=7, null=False, blank=False)
    ancho = models.IntegerField(max_digits=7, null=False, blank=False)


    def clean(self):
        if self.precio < 0:
            raise ValidationError("El precio estimado no puede ser negativo.")