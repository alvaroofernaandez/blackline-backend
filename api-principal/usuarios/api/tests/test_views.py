import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from django.urls import reverse
from api.models import User
from api.Models.CitaModel import Cita
from api.Models.DiseñoModel import Design
from api.Models.FacturaModel import Factura
from rest_framework_simplejwt.tokens import AccessToken


'''
    Tests del Usuario
'''
@pytest.mark.django_db
def test_registrar_user_ok():
    client = APIClient()
    data = {
        "username": "user1",
        "email": "user1@example.com",
        "password": "pass1234",
        "can_receive_emails": True
    }
    url = "/api/usuarios/registrar_user/"
    response = client.post(url, data, format="json")
    assert response.status_code == 201


@pytest.mark.django_db
@pytest.mark.parametrize("missing_field", ["email", "password", "can_receive_emails"])
def test_registrar_user_missing_fields(missing_field):
    client = APIClient()
    data = {
        "username": "user1",
        "email": "user1@example.com",
        "password": "pass1234",
        "can_receive_emails": True
    }
    data.pop(missing_field)
    url =  "/api/usuarios/registrar_user/"
    response = client.post(url, data)
    assert response.status_code == 400
    assert "error" in response.data


@pytest.mark.django_db
def test_registrar_user_invalid_email():
    client = APIClient()
    data = {
        "username": "user1",
        "email": "notanemail",
        "password": "pass1234",
        "can_receive_emails": True
    }
    url =  "/api/usuarios/registrar_user/"
    response = client.post(url, data)
    assert response.status_code == 400
    assert "error" in response.data

@pytest.mark.django_db
def test_registrar_user_duplicate_email():
    User.objects.create_user(username="existing", email="dup@example.com", password="pass1234")
    client = APIClient()
    data = {
        "username": "user2",
        "email": "dup@example.com",
        "password": "pass1234",
        "can_receive_emails": True
    }
    url =  "/api/usuarios/registrar_user/"
    response = client.post(url, data)
    assert response.status_code == 400
    assert "error" in response.data


@pytest.mark.django_db
def test_modificar_instagram_username_ok():
    user = User.objects.create_user(username="user", email="user@example.com", password="pass")
    client = APIClient()
    data = {"id": user.id, "instagram_username": "nuevo_username"}
    url =  "/api/usuarios/modificar-instagram-username/"
    response = client.patch(url, data)
    assert response.status_code == 200
    user.refresh_from_db()
    assert user.instagram_username == "nuevo_username"


@pytest.mark.django_db
def test_modificar_instagram_username_missing_fields():
    client = APIClient()
    url = "/api/usuarios/modificar-instagram-username/"
    response = client.patch(url, {})
    assert response.status_code == 400

@pytest.mark.django_db
def test_modificar_instagram_username_username_taken():
    user1 = User.objects.create_user(username="user1", email="user1@example.com", password="pass", instagram_username="existe")
    user2 = User.objects.create_user(username="user2", email="user2@example.com", password="pass")
    client = APIClient()
    data = {"id": user2.id, "instagram_username": "existe"}
    url = "/api/usuarios/modificar-instagram-username/"
    response = client.patch(url, data)
    assert response.status_code == 400

@pytest.mark.django_db
def test_modificar_instagram_username_user_not_found():
    client = APIClient()
    data = {"id": 9999, "instagram_username": "nuevo"}
    url = "/api/usuarios/modificar-instagram-username/"
    response = client.patch(url, data)
    assert response.status_code == 404

@pytest.mark.django_db
def test_modificar_can_receive_emails_ok():
    user = User.objects.create_user(username="user", email="user@example.com", password="pass", can_receive_emails=False)
    client = APIClient()
    data = {"id": user.id, "can_receive_emails": True}
    url = "/api/usuarios/modificar-recibir-correos/"
    response = client.patch(url, data)
    assert response.status_code == 200
    user.refresh_from_db()
    assert user.can_receive_emails is True

@pytest.mark.django_db
def test_modificar_can_receive_emails_missing_fields():
    client = APIClient()
    url = "/api/usuarios/modificar-recibir-correos/"
    response = client.patch(url, {})
    assert response.status_code == 400


@pytest.mark.django_db
def test_modificar_can_receive_emails_user_not_found():
    client = APIClient()
    data = {"id": 9999, "can_receive_emails": True}
    url = "/api/usuarios/modificar-recibir-correos/"
    response = client.patch(url, data)
    assert response.status_code == 404


@pytest.mark.django_db
def test_modificar_user_not_found():
    admin = User.objects.create_user(username="admin", email="admin@example.com", password="pass", is_staff=True)
    client = APIClient()
    client.force_authenticate(user=admin)

    data = {"id_usuario": 9999, "nombre": "NuevoNombre"}
    url = "/api/usuarios/modificar_user/"
    response = client.put(url, data, format="json")
    assert response.status_code == 404
@pytest.mark.django_db
def test_modificar_contrasena_invalid_token():
    client = APIClient()
    data = {
        "nueva_contrasena": "newpassword123",
        "token": "token_invalido"
    }
    url = "/api/usuarios/modificar_contrasena/"
    response = client.patch(url, data, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_modificar_contrasena_missing_fields():
    client = APIClient()
    data = {"nueva_contrasena": "newpassword123"}  # falta token
    url = "/api/usuarios/modificar_contrasena/"
    response = client.patch(url, data, format="json")
    assert response.status_code == 400

@pytest.mark.django_db
def test_eliminar_user_not_found():
    admin = User.objects.create_user(username="admin", email="admin@example.com", password="pass", is_staff=True)
    client = APIClient()
    client.force_authenticate(user=admin)

    url = "/api/usuarios/eliminar_user/?id_usuario=9999"
    response = client.delete(url)
    assert response.status_code == 404

'''
    Tests de Cita
'''
@pytest.mark.django_db
def test_list_citas():
    client = APIClient()
    solicitante = User.objects.create_user(username="juan123", email="juan@example.com", password="testpassword")

    image_file = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
    design = Design.objects.create(
        image=image_file,
        titulo="Design 1",
        descripcion="Descripción del diseño",
        alto=100,
        ancho=100
    )

    Cita.objects.create(fecha="2025-05-25", hora="1", solicitante=solicitante, design=design)
    Cita.objects.create(fecha="2025-05-25", hora="2", solicitante=solicitante, design=design)

    url = "/api/citas/"
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) >= 2


@pytest.mark.django_db
def test_retrieve_cita_ok():
    solicitante = User.objects.create_user(username="juan123", email="juan@example.com", password="testpassword")

    image_file = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
    design = Design.objects.create(
        image=image_file,
        titulo="Design 1",
        descripcion="Descripción del diseño",
        alto=100,
        ancho=100
    )

    cita = Cita.objects.create(fecha="2025-05-25", hora="1", solicitante=solicitante, design=design)
    client = APIClient()

    url = f"/api/citas/{cita.id}/"
    response = client.get(url)

    assert response.status_code == 200
    assert response.data['id'] == cita.id


@pytest.mark.django_db
def test_create_cita_ok():
    client = APIClient()
    solicitante = User.objects.create_user(username="juan123", email="juan@example.com", password="testpassword")

    image_file = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
    design = Design.objects.create(
        image=image_file,
        titulo="Design 1",
        descripcion="Descripción del diseño",
        alto=100,
        ancho=100
    )

    data = {
        "fecha": "2025-05-25",
        "hora": "1",
        "solicitante": solicitante.id,
        "design": design.id
    }

    url = "/api/citas/"
    response = client.post(url, data, format='json')

    assert response.status_code == 201
    assert response.data['fecha'] == data['fecha']
    assert response.data['hora'] == data['hora']


@pytest.mark.django_db
def test_get_tramo_horario_with_fecha():
    client = APIClient()
    solicitante = User.objects.create_user(username="juan123", email="juan@example.com", password="testpassword")

    image_file = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
    design = Design.objects.create(
        image=image_file,
        titulo="Design 1",
        descripcion="Descripción del diseño",
        alto=100,
        ancho=100
    )

    Cita.objects.create(fecha="2025-05-25", hora="1", solicitante=solicitante, design=design)

    url = "/api/citas/tramo_horario/"
    response = client.get(url, {'fecha': '2025-05-25'})

    assert response.status_code == 200
    assert response.data['1'] is False
    assert response.data['2'] is True

'''
    Tests de Diseño
'''