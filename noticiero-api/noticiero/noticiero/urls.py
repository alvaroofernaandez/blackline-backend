from django.contrib import admin
from django.urls import path
from api.views import NoticiasListCreateView, NoticiasDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('noticias/', NoticiasListCreateView.as_view(), name='noticias-list-create'),
    path('noticias/<str:pk>/', NoticiasDetailView.as_view(), name='noticias-detail'),
]
