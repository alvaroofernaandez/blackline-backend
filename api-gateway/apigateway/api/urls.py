from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^(?P<service_name>[\w-]+)/(?P<id>[\w-]+)/(?P<extra>[\w-]+)/$', views.route_request, name='route_request_with_extra'),

    re_path(r'^(?P<service_name>[\w-]+)/(?P<extra>[\w-]+)/(?P<extra2>[\w-]+)/$', views.route_request, name='route_request_with_extra2'),

    re_path(r'^(?P<service_name>[\w-]+)/(?P<id>[\w-]+)/$', views.route_request, name='route_request_with_id'),

    re_path(r'^facturas/detalle/$', views.route_request, {'service_name': 'detalle_facturas'}, name='facturas_detalle'),

    re_path(r'^(?P<service_name>[\w-]+)/$', views.route_request, name='route_request_without_id'),
]