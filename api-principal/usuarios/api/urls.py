from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .Views.DiseñoView import DiseñoView
from .Views.UserView import UserViewSet
from .Views.CitasView import CitasViewSet
from .Views.FacturaView import FacturaViewSet

router = DefaultRouter()
router.register(r'usuarios', UserViewSet, basename='usuarios')
router.register(r'facturas', FacturaViewSet, basename='facturas')
router.register(r'citas', CitasViewSet, basename='citas')
router.register(r'diseños', DiseñoView, basename='diseños')


urlpatterns = [
    path('', include(router.urls)),
]
