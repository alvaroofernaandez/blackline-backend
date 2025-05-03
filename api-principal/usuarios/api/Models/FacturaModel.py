from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from ..models import User
from ..Models.CitaModel import Cita

# models.py

class Factura(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='facturas')
    citas = models.ManyToManyField(Cita, related_name='facturas')
    fecha_emision = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def calcular_total(self):
        '''
        total = 0
        citas = self.citas.prefetch_related('design').all()

        for cita in citas:
            if cita.design and cita.estado == 'completada':
                total += cita.design.precio or 0

        self.total = total
        self.save()
        '''

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.calcular_total()
