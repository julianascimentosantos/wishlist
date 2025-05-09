from django.contrib import admin
from .models import Client, FavoriteProduct

admin.site.register(Client)
admin.site.register(FavoriteProduct)