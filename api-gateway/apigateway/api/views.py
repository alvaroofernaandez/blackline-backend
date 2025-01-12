import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view


@api_view(['GET', 'POST'])
def route_request(request, service_name):
    # Definimos el diccionario con los endpoints. Más tarde tendremos que pasar los endpoints a un .env
    servicios = {
        'GET': {
            'usuarios': 'http://localhost:8001/api/usuarios/',
            'noticias': 'http://localhost:8002/noticias/',
        },
        'POST': {
            'usuarios': 'http://localhost:8001/api/usuarios/registrar_User/',
        },
    }

    metodo = obtener_metodo(request)

    if metodo not in servicios or service_name not in servicios[metodo]:
        return JsonResponse({'error': 'Ruta no encontrada o método no soportado.'}, status=404)

    # La url objetivo será la de que corresponda a el diccionario servicios
    url_final = servicios[metodo][service_name]

    # Devolvemos una respuesta con todos los datos de la url o endpoint
    try:
        response = requests.request(
            method=metodo,
            url=url_final,
            headers={key: value for key, value in request.headers.items() if key != 'Host'},
            data=request.body,
            params=request.GET.dict()
        )
        return JsonResponse(response.json(), status=response.status_code, safe=False)

    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': f'Error al conectar con el microservicio: {str(e)}'}, status=500)


# Metodo para devolver el metodo utilizado y pasado a mayúsculas
def obtener_metodo(request):
    return request.method.upper()