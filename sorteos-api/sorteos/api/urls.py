from django.urls import path
from .ViewSets.ParticipanteViewSet import ParticipanteViewSet
from .ViewSets.SorteoViewSet import SorteoViewSet

urlpatterns = [
    path('sorteos/<str:sorteo_id>/participantes/', ParticipanteViewSet.as_view(), name='participantes-list-create'),

    path('sorteos/', SorteoViewSet.as_view(), name='sorteos-list-create'),
    path('sorteos/<str:sorteo_id>/', SorteoViewSet.as_view(), name='sorteos-detail-update-delete'),
    path('sorteos/<str:sorteo_id>/<str:action>/', SorteoViewSet.as_view(), name='sorteos-actions'),
]
