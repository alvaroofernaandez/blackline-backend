from bson import ObjectId
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Sorteo, Participante

class ParticipanteViewSet(APIView):

    def post(self, request, sorteo_id):
        try:
            sorteo = Sorteo.objects.get(id=ObjectId(sorteo_id))
            data = request.data

            if isinstance(data, list):
                participantes = []
                for item in data:
                    participante = Participante(
                        instagram_username=item["instagram_username"],
                        requirements=item["requirements"]
                    )
                    sorteo.participantes.append(participante)
                    participantes.append(participante)
                sorteo.save()
                return Response({"message": f"{len(participantes)} participantes añadidos correctamente"},
                                status=status.HTTP_201_CREATED)

            else:
                participante = Participante(
                    instagram_username=data["instagram_username"],
                    requirements=data["requirements"]
                )
                sorteo.participantes.append(participante)
                sorteo.save()
                return Response({"message": "Participante añadido correctamente"}, status=status.HTTP_201_CREATED)

        except Sorteo.DoesNotExist:
            return Response({"error": "Sorteo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, sorteo_id):
        try:
            sorteo = Sorteo.objects.get(id=ObjectId(sorteo_id))
            participantes = sorteo.participantes
            msgData = [{"Instagram Username": p.instagram_username, "Requirements": p.requirements} for p in participantes]
            return Response(msgData, status=status.HTTP_200_OK)
        except Sorteo.DoesNotExist:
            return Response({"error": "Sorteo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
