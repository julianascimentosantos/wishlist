from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class FavoriteProduct(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='favorites')
    product_id = models.CharField(max_length=255)

    class Meta:
        unique_together = ('client', 'product_id')

    def __str__(self):
        return f"{self.client.name} - {self.product_id}"
