from django.urls import path
from .Views.DiseñoView import DiseñoView
from .Views.UserView import UserViewSet
from .Views.CitasView import CitasViewSet

urlpatterns = [
  path('citas/', CitasViewSet.as_view(), name='citas'),
  path('citas/<int:pk>/', CitasViewSet.as_view(), name='citas'),
  path('diseños/', DiseñoView.as_view(), name='diseños'),
  path('diseños/<int:pk>/', DiseñoView.as_view(), name='diseños'),
  path('usuarios/', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='usuarios')
]
