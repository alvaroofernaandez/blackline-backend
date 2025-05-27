import requests
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from json.decoder import JSONDecodeError


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def route_request(request, service_name=None, id=None, **kwargs):
    if not service_name:
        service_name = kwargs.get('service_name')

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
            'change_password': 'http://api-principal:8001/api/send-email-password-reset/',
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
            'modificar_contrasena': 'http://api-principal:8001/api/usuarios/modificar_contrasena/',
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

    if metodo not in servicios or service_name not in servicios[metodo]:
        return JsonResponse({'error': 'Ruta no encontrada o método no soportado.'}, status=404)

    url_template = servicios[metodo][service_name]

    if '{id}' in url_template:
        if not id:
            return JsonResponse({'error': 'Se requiere un id en la solicitud.'}, status=400)
        url_final = url_template.format(id=id)
    else:
        url_final = url_template

    headers = {
        'Authorization': request.headers.get('Authorization', ''),
    }
    if 'Content-Type' in request.headers:
        headers['Content-Type'] = request.headers['Content-Type']

    try:
        response = requests.request(
            method=metodo,
            url=url_final,
            headers=headers,
            data=request.body if metodo in ['POST', 'PUT', 'PATCH', 'DELETE'] else None,
            params=request.GET.dict() if metodo == 'GET' else None
        )

        if response.status_code == 204:
            return JsonResponse({}, status=204)

        content_type = response.headers.get('Content-Type', '')
        content_disposition = response.headers.get('Content-Disposition', '')

        download = request.GET.get('download', '0')

        if download == '1' or 'attachment' in content_disposition.lower():
            if not content_disposition:
                content_disposition = 'attachment'

            resp = HttpResponse(
                response.content,
                status=response.status_code,
                content_type=content_type
            )
            resp['Content-Disposition'] = content_disposition
            return resp
        
        def replace_internal_urls(data, old, new):
            if isinstance(data, dict):
                return {k: replace_internal_urls(v, old, new) for k, v in data.items()}
            elif isinstance(data, list):
                return [replace_internal_urls(item, old, new) for item in data]
            elif isinstance(data, str) and old in data:
                return data.replace(old, new)
            return data

        if 'application/json' in content_type:
            try:
                data = response.json()

                if service_name == 'diseños' and metodo == 'GET':
                    data = replace_internal_urls(data, 'http://api-principal:8001', 'http://localhost:8001')
                elif service_name == 'noticias' and metodo == 'GET':
                    data = replace_internal_urls(data, 'http://noticiero-api:8002', 'http://localhost:8002')

                return JsonResponse(data, status=response.status_code, safe=False)
            except (UnicodeDecodeError, JSONDecodeError):
                return HttpResponse(response.content, status=response.status_code, content_type=content_type)

        return HttpResponse(
            response.content,
            status=response.status_code,
            content_type=content_type
        )

    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': f'Error al conectar con el microservicio: {str(e)}'}, status=500)
