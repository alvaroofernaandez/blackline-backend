from django.urls import path
from .views import NoticiasListCreateAPIView, NoticiasDetailAPIView

urlpatterns = [
    path('noticias/', NoticiasListCreateAPIView.as_view(), name='noticias-list-create'),
    path('noticias/<str:id>/', NoticiasDetailAPIView.as_view(), name='noticias-detail'),
]
