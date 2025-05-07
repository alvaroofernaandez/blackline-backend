from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .Views.DiseñoView import DiseñoView
from .Views.UserView import UserViewSet
from .Views.CitasView import CitasViewSet
from .Views.FacturaView import FacturaViewSet

router = DefaultRouter()
router.register(r'usuarios', UserViewSet, basename='usuarios')
router.register('facturas', FacturaViewSet, basename='facturas')

urlpatterns = [
  path('', include(router.urls)),
  path('citas/', CitasViewSet.as_view(), name='citas'),
  path('citas/<int:pk>/', CitasViewSet.as_view(), name='citas'),
  path('diseños/', DiseñoView.as_view(), name='diseños'),
  path('diseños/<int:pk>/', DiseñoView.as_view(), name='diseños'),
]
