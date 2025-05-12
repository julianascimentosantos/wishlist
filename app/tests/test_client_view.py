import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from app.models import Client
from django.contrib.auth.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", password="testpass")

@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def client_data():
    return {
        "name": "Client Test",
        "email": "client@test.com",
    }

@pytest.mark.django_db
def test_list_clients(authenticated_client):
    Client.objects.create(name="Client 1", email="c1@test.com")
    url = reverse("clients-list")
    response = authenticated_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == "Client 1"

@pytest.mark.django_db
def test_create_client(authenticated_client, client_data):
    url = reverse("clients-list")
    response = authenticated_client.post(url, client_data, format="json")

    assert response.status_code == 201
    assert Client.objects.count() == 1
    assert Client.objects.first().name == client_data["name"]

@pytest.mark.django_db
def test_get_client(authenticated_client, client_data):
    client_instance = Client.objects.create(**client_data)
    url = reverse("clients-detail", args=[client_instance.id])
    response = authenticated_client.get(url)

    assert response.status_code == 200
    assert response.data["email"] == client_data["email"]

@pytest.mark.django_db
def test_update_client(authenticated_client, client_data):
    client_instance = Client.objects.create(**client_data)
    url = reverse("clients-detail", args=[client_instance.id])
    updated_data = client_data.copy()
    updated_data["name"] = "Client Updated"

    response = authenticated_client.put(url, updated_data, format="json")

    assert response.status_code == 200
    assert response.data["name"] == "Client Updated"

@pytest.mark.django_db
def test_delete_client(authenticated_client, client_data):
    client_instance = Client.objects.create(**client_data)
    url = reverse("clients-detail", args=[client_instance.id])

    response = authenticated_client.delete(url)

    assert response.status_code == 204
    assert Client.objects.count() == 0

@pytest.mark.django_db
def test_create_client_with_invalid_data(authenticated_client):
    url = reverse("clients-list")
    invalid_data = {
        "name": "",
        "email": "email-invalid",
    }

    response = authenticated_client.post(url, invalid_data, format="json")

    assert response.status_code == 400
    assert "name" in response.data
    assert "email" in response.data

@pytest.mark.django_db
def test_get_nonexistent_client(authenticated_client):
    url = reverse("clients-detail", args=[9999])

    response = authenticated_client.get(url)

    assert response.status_code == 404

@pytest.mark.django_db
def test_update_nonexistent_client(authenticated_client):
    url = reverse("clients-detail", args=[9999])
    data = {
        "name": "New Client",
        "email": "new@email.com",
    }

    response = authenticated_client.put(url, data, format="json")

    assert response.status_code == 404

@pytest.mark.django_db
def test_delete_nonexistent_client(authenticated_client):
    url = reverse("clients-detail", args=[9999])

    response = authenticated_client.delete(url)

    assert response.status_code == 404

@pytest.mark.django_db
def test_unauthenticated_access(api_client):
    url = reverse("clients-list")
    response = api_client.get(url)

    assert response.status_code == 401
