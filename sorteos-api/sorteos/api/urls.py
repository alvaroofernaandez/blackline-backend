from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewSets.sorteoViewSet import SorteoViewSet
from .viewSets.participanteViewSet import ParticipanteViewSet

router = DefaultRouter()
router.register(r'sorteos', SorteoViewSet, basename='sorteo')

urlpatterns = [
    path('', include(router.urls)),
    path('sorteos/<str:pk>/participantes/', ParticipanteViewSet.as_view({'post': 'registrar_participantes'}), name='registrar-participantes'),
]
