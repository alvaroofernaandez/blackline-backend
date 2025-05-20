import random
from datetime import datetime

import mongoengine as me

from .participanteModel import \
    Participante  # Asegúrate de que esté en el mismo paquete

ESTADOS_SORTEOS = ('activo', 'finalizado')

class Sorteo(me.Document):
    titulo = me.StringField(required=True, min_length=1)
    descripcion = me.StringField(default='')
    fecha_inicio = me.DateTimeField(default=datetime.now)
    fecha_fin = me.DateTimeField(required=True)
    estado = me.StringField(choices=ESTADOS_SORTEOS, default='activo')
    participantes = me.ListField(me.EmbeddedDocumentField(Participante), default=list)
    ganador = me.EmbeddedDocumentField(Participante, null=True)
    premios = me.ListField(me.StringField(required=True), default=list)

    meta = {
        'ordering': ['-fecha_inicio'],
        'strict': False,
    }

    def clean(self):
        if self.fecha_inicio >= self.fecha_fin:
            raise me.ValidationError("La fecha de inicio debe ser anterior a la fecha de fin.")
        if self.estado not in ESTADOS_SORTEOS:
            raise me.ValidationError(f"Estado '{self.estado}' no válido.")

    def selecGanador(self):
        if not self.participantes:
            raise ValueError("No hay participantes en este sorteo.")
        self.ganador = random.choice(self.participantes)
        self.save()

    def asignarPremio(self, premio: str):
        if not isinstance(premio, str) or not premio.strip():
            raise ValueError("Debes asignar un premio válido (cadena no vacía).")
        self.premios.append(premio.strip())
        self.save()
