import mongoengine as me
import random

from mongoengine import EmbeddedDocumentField

estados_sorteos = ('anunciado', 'activo', 'finalizado')

class Participante(me.EmbeddedDocument):
    instagram_username = me.StringField(required=True)
    requirements = me.BooleanField(required=True)

    def clean(self):
        if not self.requirements:
            raise me.ValidationError("El participante no cumple los requisitos para participar en el sorteo.")

class Sorteo(me.Document):
    titulo = me.StringField(required=True)
    descripcion = me.StringField()
    fecha_inicio = me.DateTimeField(required=True)
    fecha_fin = me.DateTimeField(required=True)
    estado = me.StringField(choices=estados_sorteos, default='anunciado')
    participantes = me.ListField(EmbeddedDocumentField(Participante), default=[])
    ganador = me.EmbeddedDocumentField(Participante, null=True)
    premios = me.ListField(me.StringField(required=True))

    def clean(self):
        if self.fecha_inicio >= self.fecha_fin:
            raise me.ValidationError("La fecha de inicio debe ser anterior a la fecha de fin.")

    def selecGanador(self):
        if not self.participantes:
            raise ValueError("No hay participantes en este sorteo")
        self.ganador = random.choice(self.participantes)
        self.save()

    def asignarPremio(self, premio):
        if not isinstance(premio, str):
            raise ValueError("Debes asignar un premio")
        self.premios.append(premio)
        self.save()