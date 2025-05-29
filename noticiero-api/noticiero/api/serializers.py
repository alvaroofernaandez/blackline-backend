import os
import uuid
from django.conf import settings
from rest_framework import serializers
from .models import Noticias

class NoticiasSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    titulo = serializers.CharField()
    descripcion = serializers.CharField(allow_blank=True, required=False)
    imagen = serializers.ImageField(required=False, allow_null=True)
    imagen_url = serializers.SerializerMethodField()  
    imagen_original_name = serializers.CharField(read_only=True)
    fecha = serializers.DateTimeField(read_only=True)

    def get_imagen_url(self, obj):
        if obj.imagen:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(f'/media/{obj.imagen}')
            return f'/media/{obj.imagen}'
        return None

    def create(self, validated_data):
        imagen_file = validated_data.pop('imagen', None)
        instance = Noticias(**validated_data)
        
        if imagen_file:
            file_extension = os.path.splitext(imagen_file.name)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            
            media_dir = os.path.join(settings.MEDIA_ROOT, 'noticias')
            os.makedirs(media_dir, exist_ok=True)
            
            file_path = os.path.join(media_dir, unique_filename)
            with open(file_path, 'wb') as f:
                for chunk in imagen_file.chunks():
                    f.write(chunk)
            
            instance.imagen = f'noticias/{unique_filename}'
            instance.imagen_original_name = imagen_file.name
        
        instance.save()
        return instance

    def update(self, instance, validated_data):
        imagen_file = validated_data.pop('imagen', None)
        
        if imagen_file:
            if instance.imagen:
                old_file_path = os.path.join(settings.MEDIA_ROOT, instance.imagen)
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)
            
            file_extension = os.path.splitext(imagen_file.name)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            
            media_dir = os.path.join(settings.MEDIA_ROOT, 'noticias')
            os.makedirs(media_dir, exist_ok=True)
            
            file_path = os.path.join(media_dir, unique_filename)
            with open(file_path, 'wb') as f:
                for chunk in imagen_file.chunks():
                    f.write(chunk)
            
            instance.imagen = f'noticias/{unique_filename}'
            instance.imagen_original_name = imagen_file.name
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if 'imagen' in data:
            del data['imagen']
        return data