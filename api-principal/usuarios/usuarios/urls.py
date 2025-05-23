from api.Views.CustomTokenObtainView import CustomTokenObtainView
from api.Views.EmailView import (SendEmailsAPIView,
                                 SendEmailWhenPasswordResetAPIView,
                                 SendSingleEmailAPIView)
from api.Views.UserView import UserViewSet
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'usuarios', UserViewSet, basename='usuario')



schema_view = get_schema_view(
    openapi.Info(
        title="API Principal",
        default_version='v1',
        description="Documentación de la API de Principal",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@sorteos.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Incluimos las rutas generadas por el router
    path('api/', include('api.urls')),  # Incluimos las rutas adicionales definidas en api/urls.py
    path('api/token/', CustomTokenObtainView.as_view(), name='custom_token_obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/send-emails/', SendEmailsAPIView.as_view(), name='send_emails'),
    path('api/send-single-email/', SendSingleEmailAPIView.as_view(), name='send_single_email'),
    path('api/send-email-password-reset/', SendEmailWhenPasswordResetAPIView.as_view(), name='send_email_password_reset'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)