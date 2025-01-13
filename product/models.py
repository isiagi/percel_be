from django.db import models
from django.core.validators import FileExtensionValidator 

# Create your models here.
def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

class Product(models.Model):
    product_name = models.CharField(max_length=50)
    product_description = models.TextField(max_length=200)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.ImageField(
        upload_to=upload_to, 
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
        null=True,
        blank=True
        )
    product_category = models.ForeignKey('category.Category', on_delete=models.CASCADE)
    product_quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.product_name
