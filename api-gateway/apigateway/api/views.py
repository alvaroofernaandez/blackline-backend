import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view

@api_view(['GET', 'POST'])
def route_request(request, service_name):

    # Definimos el diccionario con los endpoints. Más tarde tendremos que pasar los endpoints a un .env
    servicios = {
        'GET': {
            'service1/': 'http://localhost:8001/api/usuarios/',
            'service2/': 'http://localhost:8002/noticias/',
        },
        'POST': {
            'service1/': 'http://localhost:8001/api/usuarios/registrar_User/',
        },
    }

    # Obtenemos el tipo de metodo y lo pasamos a mayusculas
    metodo = obtener_metodo(request)

    # Comprobamos si el metodo se encuentra o no en el diccionario que incluye el tipo de metodo
    if metodo not in servicios:
        return JsonResponse({'error': 'Ruta no encontrada o método no soportado.'},
                            status=404)

    for url_gateway, url_final in servicios[metodo].items():
        if service_name.startswith(url_gateway):
            target_url = url_final

            try:
                response = requests.request(
                    method=request.method,
                    url=target_url,
                    headers={key: value for key, value in request.headers.items() if key != 'Host'},
                    data=request.body,
                    params=request.GET.dict()
                )
                try:
                    json_response = response.json()
                except ValueError:
                    return JsonResponse({'error': 'Respuesta inválida desde el microservicio.'}, status=500)

                return JsonResponse(json_response, status=response.status_code, safe=False)

            except requests.exceptions.RequestException as e:
                return JsonResponse({'error': f'Error al conectar con el microservicio: {str(e)}'}, status=500)

    # Si surge algun fallo en la ruta devolvemos los siguiente
    return JsonResponse({'error': 'Ruta no encontrada o método no soportado.'}, status=404)


def obtener_metodo(request):
    return request.method.upper()