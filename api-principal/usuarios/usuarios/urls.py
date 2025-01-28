from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.Views.UserView import UserViewSet
from api.Views.CustomTokenObtainView import CustomTokenObtainView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'usuarios', UserViewSet, basename='usuario')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Incluimos las rutas generadas por el router
    path('api/', include('api.urls')),  # Incluimos las rutas adicionales definidas en api/urls.py
    path('api/token/', CustomTokenObtainView.as_view(), name='custom_token_obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
