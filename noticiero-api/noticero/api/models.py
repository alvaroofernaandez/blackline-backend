import mongoengine as me
import datetime

class Noticias(me.Document):
    titulo = me.StringField(max_length=255, required=True)
    descripcion = me.StringField()
    imagen = me.StringField()
    fecha = me.DateTimeField(default=datetime.datetime.utcnow)