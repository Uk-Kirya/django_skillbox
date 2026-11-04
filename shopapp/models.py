import os.path
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


def product_image_folder(instance: "Product", filename: str) -> str:
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('products', str(instance.pk), 'images', filename)


class Product(models.Model):
    """
    Модель Product предоставляет товар, который можно продавать в магазине
    """
    class Meta:
        ordering = ["-created_at", "price"]

    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(null=False, blank=True, db_index=True)
    image = models.ImageField(upload_to=product_image_folder, null=True, blank=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    availability = models.BooleanField(default=True)
    archived = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE, verbose_name='Создатель товара')
    test = models.CharField(max_length=255)

    @property
    def description_short(self) -> str:
        if len(self.description) < 48:
            return self.description
        return self.description[:48] + "..."

    def get_absolute_url(self):
        return reverse('shopapp:product_details', kwargs={'pk': self.pk})

    def __str__(self) -> str:
        return f'{self.name}'


class Order(models.Model):
    delivery_address = models.TextField(null=True, blank=True)
    promocode = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name="orders")
