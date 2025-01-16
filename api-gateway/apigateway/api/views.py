import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view

@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def route_request(request, service_name):
    servicios = {
        'GET': {
            'usuarios': 'http://localhost:8001/api/usuarios/',
            'diseños': 'http://localhost:8001/api/diseños/',
            'noticias': 'http://localhost:8002/noticias/',
            'sorteos': 'http://localhost:8003/api/sorteos/',
            'participantes_por_sorteo': 'http://localhost:8003/api/sorteos/{sorteo_id}/participantes/',
        },
        'POST': {
            'usuarios': 'http://localhost:8001/api/usuarios/registrar_User/',
            'sorteos': 'http://localhost:8003/api/sorteos/',
            'participantes_por_sorteo': 'http://localhost:8003/api/sorteos/{sorteo_id}/participantes/',
        },
        'PUT': {
            'noticias': 'http://localhost:8002/noticias/{id}/',
            'sorteos': 'http://localhost:8003/api/sorteos/{sorteo_id}/',
        },
        'PATCH': {
            'sorteos_seleccionar_ganador': 'http://localhost:8003/api/sorteos/{sorteo_id}/seleccionar_ganador/',
            'sorteos_asignar_premio': 'http://localhost:8003/api/sorteos/{sorteo_id}/asignar_premio/',
        },
        'DELETE': {
            'noticias': 'http://localhost:8002/noticias/{id}/',
            'sorteos': 'http://localhost:8003/api/sorteos/{sorteo_id}/',
        }
    }

    metodo = request.method.upper()

    if metodo not in servicios or service_name not in servicios[metodo]:
        return JsonResponse({'error': 'Ruta no encontrada o método no soportado.'}, status=404)

    url_final = servicios[metodo][service_name]

    url_final = url_final.format(
        id=request.GET.get('id', ''),
        sorteo_id=request.GET.get('sorteo_id', '')
    )

    # Preparar encabezados
    headers = {
        'Authorization': request.headers.get('Authorization', ''),
        'Content-Type': 'application/json'
    }

    # Hacer la petición al microservicio
    try:
        response = requests.request(
            method=metodo,
            url=url_final,
            headers=headers,
            data=request.body,
            params=request.GET.dict()
        )
        try:
            return JsonResponse(response.json(), status=response.status_code, safe=False)
        except ValueError:
            return JsonResponse({'error': 'Respuesta no es un JSON válido.'}, status=500)

    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': f'Error al conectar con el microservicio: {str(e)}'}, status=500)
