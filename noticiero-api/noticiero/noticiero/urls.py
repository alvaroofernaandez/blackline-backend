from api.views import NoticiasListCreateAPIView
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from django.urls import path
from api.views import NoticiasListCreateAPIView, NoticiasDetailAPIView

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
    path('', include('api.urls')), 
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('noticias/', NoticiasListCreateAPIView.as_view(), name='noticias-list-create'),
    path('noticias/<str:id>/', NoticiasDetailAPIView.as_view(), name='noticias-detail'),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)