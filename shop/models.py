from django.db import models

# Create your models here.
class Product(models.Model):
    """Класс товара, продаваемого в магазине"""
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    amount = models.PositiveIntegerField(default=0)

class Purchase(models.Model):
    """Класс покупки товара в магазине"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    person = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)


