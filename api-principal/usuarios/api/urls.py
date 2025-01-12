from django.urls import path
from .Views.DiseñoView import DiseñoView
from .Views.UserView import UserViewSet

urlpatterns = [
  path('diseños/', DiseñoView.as_view(), name='diseños'),
  path('diseños/<int:pk>/', DiseñoView.as_view(), name='diseños'),
  path('usuarios/', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='usuarios')
]
