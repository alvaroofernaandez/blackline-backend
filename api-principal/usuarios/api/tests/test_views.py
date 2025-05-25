import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from api.models import User
from rest_framework_simplejwt.tokens import AccessToken

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

