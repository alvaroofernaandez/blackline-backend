from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.Views.UserView import UserViewSet

router = DefaultRouter()
router.register(r'usuarios', UserViewSet, basename='usuario')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Incluimos las rutas generadas por el router
]
