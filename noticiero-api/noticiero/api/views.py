from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from .models import Noticias
from .serializers import NoticiasSerializer


class NoticiasListCreateAPIView(APIView):
    def get(self, request):
        noticias = Noticias.objects()
        serializer = NoticiasSerializer(noticias, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NoticiasSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NoticiasDetailAPIView(APIView):
    def get_object(self, id):
        try:
            return Noticias.objects.get(id=id)
        except Noticias.DoesNotExist:
            raise Http404

    def get(self, request, id):
        noticia = self.get_object(id)
        serializer = NoticiasSerializer(noticia)
        return Response(serializer.data)

    def put(self, request, id):
        noticia = self.get_object(id)
        serializer = NoticiasSerializer(noticia, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        noticia = self.get_object(id)
        noticia.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
