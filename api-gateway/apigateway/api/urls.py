from django.urls import re_path
from . import views

urlpatterns = [
    # Ruta para capturar 'service_name' y 'id'
    re_path(r'^(?P<service_name>[\w-]+)/(?P<id>[\w-]+)/$', views.route_request, name='route_request_with_id'),

    # Ruta para capturar solo 'service_name' sin 'id'
    re_path(r'^(?P<service_name>[\w-]+)/$', views.route_request, name='route_request_without_id'),
]
