from django.contrib import admin
from django.urls import path, include,re_path
from . import views

'''
    Utilizo re_path para poder hacer uso de expresiones regulares y de este modo poder filtrar correctamente segun
    lo que ha introducido el usuario
'''
urlpatterns = [
    re_path(r'^(?P<service_name>[\w-]+)/?$', views.route_request, name='route_request')
]