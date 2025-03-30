from django.urls import re_path
from . import views

urlpatterns = [
    # Ruta para capturar 'service_name' y 'sorteo_id' sin el prefijo 'api'
    re_path(r'^(?P<service_name>[\w-]+)/(?P<sorteo_id>[\w-]+)/$', views.route_request, name='route_request_with_id'),

    # Ruta para capturar solo 'service_name' sin 'sorteo_id' y sin el prefijo 'api'
    re_path(r'^(?P<service_name>[\w-]+)/$', views.route_request, name='route_request_without_id'),
]
