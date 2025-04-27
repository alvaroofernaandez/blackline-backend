from django.contrib import admin
from django.urls import path
from api.views import NoticiasListCreateView, NoticiasDetailView
from django.urls import include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="API de Noticias",
        default_version='v1',
        description="Documentación de la API de Noticias",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@sorteos.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('noticias/', NoticiasListCreateView.as_view(), name='noticias-list-create'),
    path('noticias/<str:pk>/', NoticiasDetailView.as_view(), name='noticias-detail'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]
