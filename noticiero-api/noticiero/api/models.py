import datetime
import os
from django.conf import settings
import mongoengine as me

class Noticias(me.Document):
    titulo = me.StringField(max_length=255, required=True)
    descripcion = me.StringField()
    imagen = me.StringField()  
    imagen_original_name = me.StringField()  
    fecha = me.DateTimeField(default=datetime.datetime.utcnow)

    meta = {'collection': 'noticias'}

    def delete(self, *args, **kwargs):
        if self.imagen:
            file_path = os.path.join(settings.MEDIA_ROOT, self.imagen)
            if os.path.exists(file_path):
                os.remove(file_path)
        super().delete(*args, **kwargs)