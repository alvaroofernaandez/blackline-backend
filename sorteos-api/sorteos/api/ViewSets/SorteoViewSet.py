from bson import ObjectId
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Sorteo, Participante
import mongoengine as me

class SorteoViewSet(APIView):

    def get(self, request):
        sorteos = Sorteo.objects.all()
        msgData = [
            {
                "id": str(s.id),
                "titulo": s.titulo,
                "descripcion": s.descripcion,
                "fecha_inicio": s.fecha_inicio,
                "fecha_fin": s.fecha_fin,
                "estado": s.estado,
                "ganador": str(s.ganador.id) if s.ganador else None,
                "premios": s.premios,
                "participantes": [
                    {"instagram_username": p.instagram_username}
                    for p in s.participantes
                ]
            } for s in sorteos
        ]
        # "id": str(p.id),
        return Response(msgData, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            data = request.data
            sorteo = Sorteo(
                titulo=data["titulo"],
                descripcion=data.get("descripcion", ""),
                fecha_inicio=data["fecha_inicio"],
                fecha_fin=data["fecha_fin"],
                estado=data.get("estado", "anunciado"),
                premios=data.get("premios", [])
            )
            sorteo.clean()
            sorteo.save()
            return Response({"message": "Sorteo creado correctamente", "id": str(sorteo.id)}, status=status.HTTP_200_OK)
        except me.ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, sorteo_id):
        try:
            sorteo = Sorteo.objects.get(id=ObjectId(sorteo_id))
            data = request.data
            sorteo.estado = data.get("estado", sorteo.estado)
            sorteo.clean()
            sorteo.save()
            return Response({"message": "Sorteo actualizado correctamente"}, status=status.HTTP_200_OK)
        except Sorteo.DoesNotExist:
            return Response({"error": "Sorteo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except me.ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, sorteo_id, action):
        try:
            sorteo = Sorteo.objects.get(id=ObjectId(sorteo_id))

            if action == "seleccionar_ganador":
                sorteo.selecGanador()
                sorteo.estado="finalizado"
                sorteo.save()
                return Response({"message": "Ganador seleccionado correctamente", "ganador": str(sorteo.ganador.instagram_username)}, status=status.HTTP_200_OK)

            elif action == "asignar_premio":
                premio = request.data.get("premio")
                if not premio:
                    return Response({"error": "Debes asignar un premio"}, status=status.HTTP_400_BAD_REQUEST)
                sorteo.asignarPremio(premio)
                return Response({"message": "Premio asignado correctamente", "premios": sorteo.premios}, status=status.HTTP_200_OK)

            else:
                return Response({"error": "Acción no reconocida"}, status=status.HTTP_404_NOT_FOUND)

        except Sorteo.DoesNotExist:
            return Response({"error": "Sorteo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, sorteo_id):
        try:
            sorteo = Sorteo.objects.get(id=ObjectId(sorteo_id))
            sorteo.delete()
            return Response({"message": "Sorteo eliminado correctamente"}, status=status.HTTP_200_OK)
        except Sorteo.DoesNotExist:
            return Response({"error": "Sorteo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
