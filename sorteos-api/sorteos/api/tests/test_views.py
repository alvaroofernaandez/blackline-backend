import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from bson import ObjectId
from rest_framework.test import APIClient
from rest_framework import status
import mongoengine as me

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def mock_admin_user():
    return {
        'id': 'admin_id',
        'role': 'admin',
        'username': 'admin_user'
    }

@pytest.fixture
def mock_normal_user():
    return {
        'id': 'user_id',
        'role': 'user',
        'username': 'normal_user'
    }

@pytest.fixture
def sample_sorteo_data():
    return {
        'titulo': 'Sorteo Test',
        'descripcion': 'Descripción de prueba',
        'fecha_inicio': datetime.now(),
        'fecha_fin': datetime.now() + timedelta(days=7),
        'estado': 'activo',
        'premios': ['Premio 1', 'Premio 2']
    }

@pytest.fixture
def sample_participante_data():
    return {
        'instagram_username': 'test_user',
        'requirements': True
    }

@pytest.fixture
def mock_sorteo():
    sorteo = MagicMock()
    sorteo.id = ObjectId()
    sorteo.titulo = 'Sorteo Test'
    sorteo.descripcion = 'Descripción test'
    sorteo.fecha_inicio = datetime.now()
    sorteo.fecha_fin = datetime.now() + timedelta(days=7)
    sorteo.estado = 'activo'
    sorteo.participantes = []
    sorteo.ganador = None
    sorteo.premios = ['Premio 1']
    return sorteo

@pytest.fixture
def mock_participante():
    participante = MagicMock()
    participante.instagram_username = 'test_user'
    participante.requirements = True
    return participante

class TestSorteoViewSet:
    @patch('api.viewSets.sorteoViewSet.Sorteo')
    def test_list_sorteos_success(self, mock_sorteo_model, api_client):
        mock_sorteo_model.objects.all.return_value = []
        response = api_client.get('/api/sorteos/')
        assert response.status_code == status.HTTP_200_OK
        mock_sorteo_model.objects.all.assert_called_once()

    @patch('api.viewSets.sorteoViewSet.Sorteo')
    def test_retrieve_sorteo_success(self, mock_sorteo_model, api_client, mock_sorteo):
        sorteo_id = str(ObjectId())
        mock_sorteo_model.objects.get.return_value = mock_sorteo
        response = api_client.get(f'/api/sorteos/{sorteo_id}/')
        assert response.status_code == status.HTTP_200_OK

    @patch('api.viewSets.sorteoViewSet.Sorteo')
    def test_retrieve_sorteo_not_found(self, mock_sorteo_model, api_client):
        sorteo_id = str(ObjectId())
        mock_sorteo_model.objects.get.side_effect = me.DoesNotExist()
        response = api_client.get(f'/api/sorteos/{sorteo_id}/')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'error' in response.data

    @patch('api.viewSets.sorteoViewSet.IsAdminUser')
    @patch('api.viewSets.sorteoViewSet.Sorteo')
    def test_create_sorteo_success(self, mock_sorteo_model, mock_admin_permission, 
                                api_client, sample_sorteo_data, mock_admin_user):
        mock_admin_permission.return_value.has_permission.return_value = True
        api_client.force_authenticate(user=mock_admin_user)
        mock_sorteo_instance = MagicMock()
        mock_sorteo_instance.id = ObjectId()
        mock_sorteo_model.return_value = mock_sorteo_instance
        response = api_client.post('/api/sorteos/', data=sample_sorteo_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert 'message' in response.data
        assert 'id' in response.data

    @patch('api.viewSets.sorteoViewSet.IsAdminUser')
    def test_create_sorteo_invalid_data(self, mock_admin_permission, api_client, mock_admin_user):
        mock_admin_permission.return_value.has_permission.return_value = True
        api_client.force_authenticate(user=mock_admin_user)
        invalid_data = {
            'titulo': '',  
            'fecha_inicio': datetime.now() + timedelta(days=1),
            'fecha_fin': datetime.now(),
        }
        response = api_client.post('/api/sorteos/', data=invalid_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('api.viewSets.sorteoViewSet.IsAdminUser')
    @patch('api.viewSets.sorteoViewSet.Sorteo')
    def test_update_sorteo_success(self, mock_sorteo_model, mock_admin_permission, api_client, mock_admin_user, sample_sorteo_data):
        sorteo_id = str(ObjectId())
        mock_admin_permission.return_value.has_permission.return_value = True
        api_client.force_authenticate(user=mock_admin_user)
        mock_instance = MagicMock()
        mock_sorteo_model.objects.get.return_value = mock_instance
        response = api_client.put(f'/api/sorteos/{sorteo_id}/', data=sample_sorteo_data, format='json')
        assert response.status_code in (status.HTTP_200_OK, status.HTTP_204_NO_CONTENT)

    @patch('api.viewSets.sorteoViewSet.IsAdminUser')
    @patch('api.viewSets.sorteoViewSet.Sorteo')
    def test_update_sorteo_not_found(self, mock_sorteo_model, mock_admin_permission, api_client, mock_admin_user, sample_sorteo_data):
        sorteo_id = str(ObjectId())
        mock_admin_permission.return_value.has_permission.return_value = True
        api_client.force_authenticate(user=mock_admin_user)
        mock_sorteo_model.objects.get.side_effect = me.DoesNotExist()
        response = api_client.put(f'/api/sorteos/{sorteo_id}/', data=sample_sorteo_data, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('api.viewSets.sorteoViewSet.IsAdminUser')
    @patch('api.viewSets.sorteoViewSet.Sorteo')
    def test_destroy_sorteo_success(self, mock_sorteo_model, mock_admin_permission, api_client, mock_admin_user):
        sorteo_id = str(ObjectId())
        mock_admin_permission.return_value.has_permission.return_value = True
        api_client.force_authenticate(user=mock_admin_user)
        mock_instance = MagicMock()
        mock_sorteo_model.objects.get.return_value = mock_instance
        response = api_client.delete(f'/api/sorteos/{sorteo_id}/')
        assert response.status_code == status.HTTP_200_OK

    @patch('api.viewSets.sorteoViewSet.IsAdminUser')
    @patch('api.viewSets.sorteoViewSet.Sorteo')
    def test_destroy_sorteo_not_found(self, mock_sorteo_model, mock_admin_permission, api_client, mock_admin_user):
        sorteo_id = str(ObjectId())
        mock_admin_permission.return_value.has_permission.return_value = True
        api_client.force_authenticate(user=mock_admin_user)
        mock_sorteo_model.objects.get.side_effect = me.DoesNotExist()
        response = api_client.delete(f'/api/sorteos/{sorteo_id}/')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('api.viewSets.sorteoViewSet.IsAdminUser')
    @patch('api.viewSets.sorteoViewSet.Sorteo')
    def test_seleccionar_ganador_success(self, mock_sorteo_model, mock_admin_permission, api_client, mock_admin_user, mock_sorteo):
        sorteo_id = str(ObjectId())
        mock_admin_permission.return_value.has_permission.return_value = True
        api_client.force_authenticate(user=mock_admin_user)
        mock_sorteo_model.objects.get.return_value = mock_sorteo
        mock_sorteo.selecGanador.return_value = None
        mock_sorteo.ganador = MagicMock(instagram_username='winner_user')
        response = api_client.patch(f'/api/sorteos/{sorteo_id}/seleccionar_ganador/')
        assert response.status_code == status.HTTP_200_OK
        assert 'ganador' in response.data

    @patch('api.viewSets.sorteoViewSet.IsAdminUser')
    @patch('api.viewSets.sorteoViewSet.Sorteo')
    def test_seleccionar_ganador_no_participantes(self, mock_sorteo_model, mock_admin_permission, api_client, mock_admin_user, mock_sorteo):
        sorteo_id = str(ObjectId())
        mock_admin_permission.return_value.has_permission.return_value = True
        api_client.force_authenticate(user=mock_admin_user)
        mock_sorteo_model.objects.get.return_value = mock_sorteo
        mock_sorteo.selecGanador.side_effect = ValueError("No hay participantes en este sorteo.")
        response = api_client.patch(f'/api/sorteos/{sorteo_id}/seleccionar_ganador/')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data

    @patch('api.viewSets.sorteoViewSet.IsAdminUser')
    @patch('api.viewSets.sorteoViewSet.Sorteo')
    def test_asignar_premio_success(self, mock_sorteo_model, mock_admin_permission, api_client, mock_admin_user, mock_sorteo):
        sorteo_id = str(ObjectId())
        mock_admin_permission.return_value.has_permission.return_value = True
        api_client.force_authenticate(user=mock_admin_user)
        mock_sorteo_model.objects.get.return_value = mock_sorteo
        response = api_client.patch(f'/api/sorteos/{sorteo_id}/asignar_premio/', data={'premio': 'Premio Extra'}, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'premios' in response.data

    @patch('api.viewSets.sorteoViewSet.IsAdminUser')
    @patch('api.viewSets.sorteoViewSet.Sorteo')
    def test_asignar_premio_invalid(self, mock_sorteo_model, mock_admin_permission, api_client, mock_admin_user, mock_sorteo):
        sorteo_id = str(ObjectId())
        mock_admin_permission.return_value.has_permission.return_value = True
        api_client.force_authenticate(user=mock_admin_user)
        mock_sorteo_model.objects.get.return_value = mock_sorteo
        mock_sorteo.asignarPremio.side_effect = ValueError("Debes asignar un premio válido (cadena no vacía).")
        response = api_client.patch(f'/api/sorteos/{sorteo_id}/asignar_premio/', data={'premio': ''}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data

