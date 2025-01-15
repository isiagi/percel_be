from django.db import models
from django.core.validators import FileExtensionValidator 
from django.contrib.auth.models import User
from category.models import Category
from django.db.models import Sum

# Create your models here.
def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)
    


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    initial_stock = models.PositiveIntegerField(null=True, blank=True, default=0)
    available_stock = models.PositiveIntegerField()
    reorder_point = models.PositiveIntegerField(default=10)  # Alert when stock reaches this level
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:  # If new product
            print(self.initial_stock)
            self.available_stock = self.initial_stock
        super().save(*args, **kwargs)

    @property
    def stock_status(self):
        if self.available_stock <= 0:
            return "Out of Stock"
        elif self.available_stock <= self.reorder_point:
            return "Low Stock"
        return "In Stock"
