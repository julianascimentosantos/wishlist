from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from app.views.client import ClientViewSet
from app.views.favorites import FavoriteProductView

router = DefaultRouter()
router.register(r'api/clients', ClientViewSet, basename='clients')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', obtain_auth_token, name='api_token_auth'),
    path('', include(router.urls)),
    path('api/clients/<int:client_id>/favorites/', FavoriteProductView.as_view(), name='client-favorites'),
    path('api/clients/<int:client_id>/favorites/<str:product_id>/', FavoriteProductView.as_view(), name='client-favorite-detail'),
]
