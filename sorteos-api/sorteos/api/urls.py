from django.urls import path
from .ViewSets.ParticipanteViewSet import ParticipanteViewSet

urlpatterns = [
    path('sorteos/<str:sorteo_id>/participantes/', ParticipanteViewSet.as_view(), name='participantes-list-create'),
]
