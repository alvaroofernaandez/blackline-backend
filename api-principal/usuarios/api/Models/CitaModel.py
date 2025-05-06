from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from ..models import User
from ..Models.DiseñoModel import Design


class Cita(models.Model):
    solicitante = models.ForeignKey(User, on_delete=models.CASCADE, related_name='citas')
    design = models.ForeignKey(Design, on_delete=models.SET_NULL, null=True, blank=True, related_name='citas'),
    fecha = models.DateField(verbose_name="Fecha de la cita")
    hora = models.CharField(max_length=1,
        choices=[
        ("1","09:00-11:00"),
        ("2","11:00-13:00"),
        ("3","15:00-17:00"),
        ("4","17:00-19:00"),
    ])
    estado = models.CharField(
        max_length=50,
        choices=[
            ('pendiente', 'Pendiente'),
            ('confirmada', 'Confirmada'),
            ('completada', 'Completada'),
            ('cancelada', 'Cancelada'),
        ],
        default='pendiente'
    )
    descripcion = models.TextField(blank=True, verbose_name="Descripción adicional")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    def __str__(self):
        return f"Cita de {self.solicitante.nombre} con diseño {self.design.titulo if self.design else 'pendiente'} el {self.fecha} a las {self.hora}"

    def clean(self):
        if self.fecha < date.today():
            raise ValidationError("La fecha de la cita no puede estar en el pasado.")

        if not self.design and not self.descripcion:
            raise ValidationError("Debes asociar un diseño existente o incluir una descripción del diseño solicitado.")