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

urlpatterns = [
    path('', include(router.urls)),
    path('diseños/', DiseñoView.as_view(), name='diseños'),
    path('diseños/<int:pk>/', DiseñoView.as_view(), name='diseños'),
]
