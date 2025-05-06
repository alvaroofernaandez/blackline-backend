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

    '''
    def calcular_total(self):
        total = 0
        if self.cita and self.cita.design and self.cita.estado == 'completada':
            total = self.cita.design.precio or 0
        self.total = total
        self.save(update_fields=['total'])
    '''
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        '''self.calcular_total()'''
