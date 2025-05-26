from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Noticias  # <-- Ajusta el import aquí

class NoticiasAPITests(APITestCase):
    
    def setUp(self):
        Noticias.drop_collection()  # Esta es la forma correcta con MongoEngine
        self.noticia1 = Noticias.objects.create(titulo='Noticia 1', descripcion='Contenido de Noticia 1')
        self.noticia2 = Noticias.objects.create(titulo='Noticia 2', descripcion='Contenido de Noticia 2')


    def test_get_noticias_list(self):
        url = reverse('noticias-list-create')  # Asegúrate de tener este nombre en tu urls.py
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_noticia(self):
        url = reverse('noticias-list-create')
        data = {'titulo': 'Nueva Noticia', 'descripcion': 'descripcion nuevo'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Noticias.objects.count(), 3)
        ultima = Noticias.objects.order_by('-id').first()
        self.assertEqual(ultima.titulo, 'Nueva Noticia')

    def test_get_noticia_detail(self):
        url = reverse('noticias-detail', kwargs={'id': self.noticia1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['titulo'], self.noticia1.titulo)

    def test_update_noticia(self):
        url = reverse('noticias-detail', kwargs={'id': self.noticia1.id})
        data = {'titulo': 'Actualizada', 'descripcion': 'descripcion actualizado'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.noticia1.reload()
        self.assertEqual(self.noticia1.titulo, 'Actualizada')

    def test_delete_noticia(self):
        url = reverse('noticias-detail', kwargs={'id': self.noticia1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Noticias.objects.filter(id=self.noticia1.id).count(), 0)
