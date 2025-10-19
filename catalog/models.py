from django.db import models
from users.models import User


class Product(models.Model):
    """ Создаем модель для товаров"""

    name = models.CharField(max_length=255, verbose_name="Название товара")
    model = models.CharField(max_length=255, verbose_name="Модель")
    description = models.TextField(null=True, blank=True, verbose_name="Описание товара")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена товара")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name