import requests
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view

@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def route_request(request, service_name=None, id=None, **kwargs):
    if not service_name:
        service_name = kwargs.get('service_name')

    # Definición de servicios
    servicios = {
        'GET': {
            'usuarios': 'http://api-principal:8001/api/usuarios/',
            'facturas': 'http://api-principal:8001/api/facturas/',
            'detalle_facturas': 'http://api-principal:8001/api/facturas/detalle/',
            'principal_documentacion': 'http://api-principal:8001/swagger/?format=openapi',
            'usuario_por_id': 'http://api-principal:8001/api/usuarios/buscar_User/?id_usuario={id}',
            'usuarios_antiguos': 'http://api-principal:8001/api/usuarios/usuariosAntiguos/?limit={limit}',
            'diseños': 'http://api-principal:8001/api/diseños/',
            'diseño_por_id': 'http://api-principal:8001/api/diseños/{id}/',
            'citas': 'http://api-principal:8001/api/citas/',
            'cita_por_id': 'http://api-principal:8001/api/citas/{id}/',
            'citas_tramo_horario': 'http://api-principal:8001/api/citas/tramo_horario/',
            'noticias': 'http://noticiero-api:8002/noticias/',
            'noticias_por_id': 'http://noticiero-api:8002/noticias/{id}/',
            'noticias_documentacion': 'http://noticiero-api:8002/swagger/?format=openapi',
            'sorteos': 'http://sorteos-api:8003/api/sorteos/',
            'sorteo_por_id': 'http://sorteos-api:8003/api/sorteos/{id}/',
            'sorteos_documentacion': 'http://sorteos-api:8003/swagger/?format=openapi',
            'participantes_por_sorteo': 'http://sorteos-api:8003/api/sorteos/{id}/participantes/',
        },
        'POST': {
            'usuarios': 'http://api-principal:8001/api/usuarios/registrar_User/',
            'facturas': 'http://api-principal:8001/api/facturas/',
            'enviar_correos_masivos': 'http://api-principal:8001/api/send-emails/',
            'enviar_correos_personalizados': 'http://api-principal:8001/api/send-single-email/',
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
            'modificar_recibir_correos': 'http://api-principal:8001/api/usuarios/modificar-recibir-correos/',
            'modificar_nombre_instagram': 'http://api-principal:8001/api/usuarios/modificar-instagram-username/',
            'sorteos_seleccionar_ganador': 'http://sorteos-api:8003/api/sorteos/{id}/seleccionar_ganador/',
            'sorteos_asignar_premio': 'http://sorteos-api:8003/api/sorteos/{id}/asignar_premio/',
        },
        'DELETE': {
            'usuarios': 'http://api-principal:8001/api/usuarios/eliminar_User/?id_usuario={id}',
            'diseño_por_id': 'http://api-principal:8001/api/diseños/{id}/',
            'cita_por_id': 'http://api-principal:8001/api/citas/{id}/',
            'noticias': 'http://noticiero-api:8002/noticias/{id}/',
            'sorteos': 'http://sorteos-api:8003/api/sorteos/{id}/',
            'facturas': 'http://api-principal:8001/api/facturas/{id}/',
        }
    }

    metodo = request.method.upper()

    # Verificación de si la ruta y método existen en los servicios
    if metodo not in servicios or service_name not in servicios[metodo]:
        return JsonResponse({'error': 'Ruta no encontrada o método no soportado.'}, status=404)

    url_template = servicios[metodo][service_name]

    # Si la URL contiene '{id}', verificamos si se proporcionó un 'id' y lo formateamos
    if '{id}' in url_template:
        if not id:
            return JsonResponse({'error': 'Se requiere un id en la solicitud.'}, status=400)
        url_final = url_template.format(id=id)
    else:
        url_final = url_template

    headers = {
        'Authorization': request.headers.get('Authorization', ''),
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request(
            method=metodo,
            url=url_final,
            headers=headers,
            data=request.body if metodo in ['POST', 'PUT', 'PATCH', 'DELETE'] else None,
            params=request.GET.dict() if metodo == 'GET' else None
        )

        # Verificar si la respuesta es 204 (sin contenido)
        if response.status_code == 204:
            return JsonResponse({}, status=204)

        content_type = response.headers.get('Content-Type', '')
        content_disposition = response.headers.get('Content-Disposition', '')

        # Verificar si se está pidiendo una descarga
        download = request.GET.get('download', '0')

        # Si 'download=1', forzamos la descarga
        if download == '1' or 'attachment' in content_disposition:
            if not content_disposition:
                content_disposition = 'attachment'

            resp = HttpResponse(
                response.content,
                status=response.status_code,
                content_type=content_type
            )
            resp['Content-Disposition'] = content_disposition
            return resp

        # Si no es descarga, devolvemos la respuesta en formato JSON
        if 'application/json' in content_type:
            return JsonResponse(response.json(), status=response.status_code, safe=False)

        # En caso contrario, simplemente devolvemos el contenido tal cual
        return HttpResponse(
            response.content,
            status=response.status_code,
            content_type=content_type
        )

    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': f'Error al conectar con el microservicio: {str(e)}'}, status=500)
