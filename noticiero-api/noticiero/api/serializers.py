from rest_framework_mongoengine.serializers import DocumentSerializer

from .models import Noticias


class NoticiasSerializer(DocumentSerializer):
    class Meta:
        model = Noticias
        fields = '__all__'
