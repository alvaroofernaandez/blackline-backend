import requests
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view

@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def route_request(request, service_name, id=None):
    # Definir las rutas de los microservicios
    servicios = {
        'GET': {
            'usuarios': 'http://api-principal:8001/api/usuarios/',
            'usuario_por_id': 'http://api-principal:8001/api/usuarios/buscar_User/?id_usuario={id}',
            'usuarios_antiguos': 'http://api-principal:8001/api/usuarios/usuariosAntiguos/?limit={limit}',
            # Cambio aquí
            'diseños': 'http://api-principal:8001/api/diseños/',
            'diseño_por_id': 'http://api-principal:8001/api/diseños/{id}/',
            'citas': 'http://api-principal:8001/api/citas/',
            'cita_por_id': 'http://api-principal:8001/api/citas/{id}/',
            'noticias': 'http://noticiero-api:8002/noticias/',
            'noticias_por_id': 'http://noticiero-api:8002/noticias/{id}/',
            'sorteos': 'http://sorteos-api:8003/api/sorteos/',
            'sorteo_por_id': 'http://sorteos-api:8003/api/sorteos/{id}/',
            'participantes_por_sorteo': 'http://sorteos-api:8003/api/sorteos/{id}/participantes/',
        },
        'POST': {
            'usuarios': 'http://api-principal:8001/api/usuarios/registrar_User/',
            'diseños': 'http://api-principal:8001/api/diseños/',
            'citas': 'http://api-principal:8001/api/citas/',
            'noticias': 'http://noticiero-api:8002/noticias/',
            'sorteos': 'http://sorteos-api:8003/api/sorteos/',
            'participantes_por_sorteo': 'http://sorteos-api:8003/api/sorteos/{id}/participantes/',
            'token': 'http://api-principal:8001/api/token/',
            'token_refresh': 'http://api-principal:8001/api/token/refresh/',
        },
        'PUT': {
            'usuarios': 'http://api-principal:8001/api/usuarios/modificar_User/',
            'diseño_por_id': 'http://api-principal:8001/api/diseños/{id}/',
            'cita_por_id': 'http://api-principal:8001/api/citas/{id}/',
            'noticias': 'http://noticiero-api:8002/noticias/{id}/',
            'sorteos': 'http://sorteos-api:8003/api/sorteos/{id}/',
        },
        'PATCH': {
            'sorteos_seleccionar_ganador': 'http://sorteos-api:8003/api/sorteos/{id}/seleccionar_ganador/',
            'sorteos_asignar_premio': 'http://sorteos-api:8003/api/sorteos/{id}/asignar_premio/',
        },
        'DELETE': {
            'usuarios': 'http://api-principal:8001/api/usuarios/eliminar_User/?id_usuario={id}',
            'diseño_por_id': 'http://api-principal:8001/api/diseños/{id}/',
            'cita_por_id': 'http://api-principal:8001/api/citas/{id}/',
            'noticias': 'http://noticiero-api:8002/noticias/{id}/',
            'sorteos': 'http://sorteos-api:8003/api/sorteos/{id}/',
        }
    }

    metodo = request.method.upper()

    # Verificar si el servicio y el método están definidos
    if metodo not in servicios or service_name not in servicios[metodo]:
        return JsonResponse({'error': 'Ruta no encontrada o método no soportado.'}, status=404)

    # Obtener la URL base correspondiente al servicio
    url_final = servicios[metodo][service_name]

    # Si es PUT, PATCH o DELETE, asegúrate de que 'id' está presente
    if '{id}' in url_final and not id:
        return JsonResponse({'error': 'Se requiere un id en la solicitud.'}, status=400)

    # Reemplazar 'id' en la URL final
    if id:
        url_final = url_final.format(id=id)

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

        if response.status_code == 204:
            return JsonResponse({}, status=204)
        # Intentar devolver la respuesta en JSON
        try:
            return JsonResponse(response.json(), status=response.status_code, safe=False)
        except ValueError:
            return JsonResponse({'error': 'Respuesta no es un JSON válido.', 'status': response.status_code}, status=500)

    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': f'Error al conectar con el microservicio: {str(e)}'}, status=500)
