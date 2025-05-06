from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from ..models import User
from ..Models.CitaModel import Cita

class Factura(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='facturas')
    cita = models.OneToOneField(Cita, on_delete=models.CASCADE, related_name='factura')
    fecha_emision = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        if self.cita and self.cita.design and self.cita.design.precio:
            self.total = self.cita.design.precio
        else:
            self.total = 0.00

        super().save(*args, **kwargs)