import requests
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view

@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def route_request(request, service_name, sorteo_id=None):
    # Definir las rutas de los microservicios
    servicios = {
        'GET': {
            'usuarios': 'http://localhost:8001/api/usuarios/',
            'diseños': 'http://localhost:8001/api/diseños/',
            'noticias': 'http://localhost:8002/noticias/',
            'noticias_por_id': 'http://localhost:8002/noticias/{sorteo_id}/',
            'sorteos': 'http://localhost:8003/api/sorteos/',
            'participantes_por_sorteo': 'http://localhost:8003/api/sorteos/{sorteo_id}/participantes/',
        },
        'POST': {
            'usuarios': 'http://localhost:8001/api/usuarios/registrar_User/',
            'noticias': 'http://localhost:8002/noticias/',
            'sorteos': 'http://localhost:8003/api/sorteos/',
            'participantes_por_sorteo': 'http://localhost:8003/api/sorteos/{sorteo_id}/participantes/',
        },
        'PUT': {
            'noticias': 'http://localhost:8002/noticias/{sorteo_id}/',
            'sorteos': 'http://localhost:8003/api/sorteos/{sorteo_id}/',  # Usar {sorteo_id} dinámicamente
        },
        'PATCH': {
            'sorteos_seleccionar_ganador': 'http://localhost:8003/api/sorteos/{sorteo_id}/seleccionar_ganador/',
            'sorteos_asignar_premio': 'http://localhost:8003/api/sorteos/{sorteo_id}/asignar_premio/',
        },
        'DELETE': {
            'noticias': 'http://localhost:8002/noticias/{sorteo_id}/',
            'sorteos': 'http://localhost:8003/api/sorteos/{sorteo_id}/',
        }
    }

    metodo = request.method.upper()

    # Verificar si el servicio y el método están definidos
    if metodo not in servicios or service_name not in servicios[metodo]:
        return JsonResponse({'error': 'Ruta no encontrada o método no soportado.'}, status=404)

    # Obtener la URL base correspondiente al servicio
    url_final = servicios[metodo][service_name]

    # Si es PUT, PATCH o DELETE, asegúrate de que 'sorteo_id' está presente
    if '{sorteo_id}' in url_final and not sorteo_id:
        return JsonResponse({'error': 'Se requiere un sorteo_id en la solicitud.'}, status=400)

    # Reemplazar 'sorteo_id' en la URL final
    if sorteo_id:
        url_final = url_final.format(sorteo_id=sorteo_id)

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
            data=request.body if metodo in ['POST', 'PUT', 'PATCH'] else None,
            params=request.GET.dict() if metodo == 'GET' else None
        )

        # Intentar devolver la respuesta en JSON
        try:
            return JsonResponse(response.json(), status=response.status_code, safe=False)
        except ValueError:
            return JsonResponse({'error': 'Respuesta no es un JSON válido.', 'status': response.status_code}, status=500)

    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': f'Error al conectar con el microservicio: {str(e)}'}, status=500)
