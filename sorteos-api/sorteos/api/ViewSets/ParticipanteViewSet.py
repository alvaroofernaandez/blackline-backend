import mongoengine as me
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Sorteo
from ..models import Participante as p


class ParticipanteViewSet(APIView):

    def post(self, request, sorteo_id):
        try:
            sorteo = Sorteo.objects.get(id=sorteo_id)
            data = request.data
            participante = p(
                instagram_username = data["instagram_username"],
                requirements = data["requirements"]
            )
            participante.clean()
            participante.save()

            sorteo.participantes.append(participante)
            sorteo.save()
            msgData = {"message": "Participante añadido correctamente"}
            return Response({msgData}, status=status.HTTP_201_CREATED)
        except Sorteo.DoesNotExist:
            msgData = {"message": "Sorteo no encontrado"}
            return Response({msgData}, status=status.HTTP_404_NOT_FOUND)
        except me.ValidationError as e:
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, sorteo_id):
        try:
            sorteo = Sorteo.objects.get(id=sorteo_id)
            participantes = sorteo.participantes
            msgData = [{"id": str(p.id), "Username Instagram": p.instagram_username} for p in participantes]
            return Response(msgData, status=status.HTTP_200_OK)
        except Sorteo.DoesNotExist:
            msgData = {"error": "Sorteo no encontrado"}
            return Response(msgData, status=status.HTTP_404_NOT_FOUND)