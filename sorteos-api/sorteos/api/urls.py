from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .viewSets.participanteViewSet import ParticipanteViewSet
from .viewSets.sorteoViewSet import SorteoViewSet

router = DefaultRouter()
router.register(r'sorteos', SorteoViewSet, basename='sorteo')

urlpatterns = [
    path('', include(router.urls)),
    path('sorteos/<str:pk>/participantes/', ParticipanteViewSet.as_view({'post': 'registrar_participantes'}), name='registrar-participantes'),
]
