from django.db import models
from customer.models import Customer
from product.models import Product
from users.models import CustomUser as User
from stock.models import StockMovement
from django.db.models import Sum, F

# Create your models here.
class Sale(models.Model):
    PAYMENT_METHODS = [
        ('CASH', 'Cash'),
        ('CARD', 'Card'),
        ('TRANSFER', 'Bank Transfer')
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='sales')
    sale_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    @property
    def total_amount(self):
        """
        Calculate total amount of the sale by summing the total price of each item
        Uses database aggregation for better performance
        """
        return self.items.aggregate(
            total=Sum(F('quantity') * F('price'))
        )['total'] or 0

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Only on creation
            # Create stock movement for the sale
            StockMovement.objects.create(
                product=self.product,
                movement_type='OUT',
                quantity=self.quantity,
                reference=f'Sale #{self.sale.id}'
            )
        super().save(*args, **kwargs)
