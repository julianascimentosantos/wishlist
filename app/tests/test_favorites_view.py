import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from app.models import Client, FavoriteProduct
from unittest.mock import patch, MagicMock

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(username='user', password='test123')

@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def client_instance():
        return Client.objects.create(name="Test", email="test@test.com")

@pytest.mark.django_db
@patch("app.views.favorites.get_products_by_id")
def test_add_product_success(mock_get_product, auth_client, client_instance):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": "1", "title": "Product"}
    mock_get_product.return_value = mock_response

    url = reverse('client-favorites', kwargs={"client_id": client_instance.id})
    response = auth_client.post(url, data={"product_id": "1"}, format="json")

    assert response.status_code == 201
    assert response.data["product_id"] == "1"

@pytest.mark.django_db
def test_add_product_missing_product_id(auth_client, client_instance):
    url = reverse('client-favorites', kwargs={"client_id": client_instance.id})
    response = auth_client.post(url, data={}, format="json")

    assert response.status_code == 400
    assert "product_id is required" in response.data["error"]

@pytest.mark.django_db
@patch("app.views.favorites.get_products_by_id")
def test_add_product_already_exists(mock_get_product, auth_client, client_instance):
    FavoriteProduct.objects.create(client=client_instance, product_id="1")

    url = reverse('client-favorites', kwargs={"client_id": client_instance.id})
    response = auth_client.post(url, data={"product_id": "1"}, format="json")

    assert response.status_code == 400
    assert "already in wishlist" in response.data["error"]

@pytest.mark.django_db
@patch("app.views.favorites.get_products_by_id")
def test_add_product_not_found_external_api(mock_get_product, auth_client, client_instance):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get_product.return_value = mock_response

    url = reverse('client-favorites', kwargs={"client_id": client_instance.id})
    response = auth_client.post(url, data={"product_id": "999"}, format="json")

    assert response.status_code == 404
    assert "not found" in response.data["error"]

@pytest.mark.django_db
@patch("app.views.favorites.get_products_by_id")
def test_get_favorites_success(mock_get_product, auth_client, client_instance):
    FavoriteProduct.objects.create(client=client_instance, product_id="1")
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": "1", "title": "Product", "image": "url", "price": 123.45
    }
    mock_get_product.return_value = mock_response

    url = reverse('client-favorites', kwargs={"client_id": client_instance.id})
    response = auth_client.get(url)

    assert response.status_code == 200
    assert isinstance(response.data, list)
    assert response.data[0]["title"] == "Product"

@pytest.mark.django_db
@patch("app.views.favorites.get_products_by_id")
def test_get_favorites_product_not_found(mock_get_product, auth_client, client_instance):
    FavoriteProduct.objects.create(client=client_instance, product_id="not_found")

    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get_product.return_value = mock_response

    url = reverse('client-favorites', kwargs={"client_id": client_instance.id})
    response = auth_client.get(url)

    assert response.status_code == 200
    assert response.data[0]["error"] == "Product not found"

@pytest.mark.django_db
def test_delete_favorite_success(auth_client, client_instance):
    FavoriteProduct.objects.create(client=client_instance, product_id="1")
    url = reverse('client-favorite-detail', kwargs={"client_id": client_instance.id, "product_id": "1"})
    response = auth_client.delete(url)

    assert response.status_code == 204

@pytest.mark.django_db
def test_delete_favorite_not_found(auth_client, client_instance):
    url = reverse('client-favorite-detail', kwargs={"client_id": client_instance.id, "product_id": "999"})
    response = auth_client.delete(url)

    assert response.status_code == 404
    assert "not found" in response.data["error"].lower()
