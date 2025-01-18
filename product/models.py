from django.db import models
from django.core.validators import FileExtensionValidator 
from users.models import CustomUser as User
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
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # initial_stock = models.PositiveIntegerField(null=True, blank=True, default=0)
    # available_stock = models.PositiveIntegerField()
    cbm = models.FloatField(null=True, blank=True)
    supplier = models.ForeignKey('supplier.Supplier', on_delete=models.SET_NULL, null=True, blank=True)
    reorder_point = models.PositiveIntegerField(default=10)  # Alert when stock reaches this level
    image = models.ImageField(upload_to=upload_to, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

    @property
    def available_stock(self):
        """Calculate current stock based on all stock movements"""
        total_in = self.stock_movements.filter(
            movement_type='IN'
        ).aggregate(total=Sum('quantity'))['total'] or 0
        
        total_out = self.stock_movements.filter(
            movement_type='OUT'
        ).aggregate(total=Sum('quantity'))['total'] or 0
        
        return total_in - total_out

    @property
    def initial_stock(self):
        """Get the initial stock from first stock movement"""
        initial = self.stock_movements.filter(
            movement_type='IN', 
            reference='Initial Stock'
        ).first()
        return initial.quantity if initial else 0

    @property
    def stock_status(self):
        current_stock = self.available_stock
        reorder_point = int(self.reorder_point)
        if current_stock <= 0:
            return "Out of Stock"
        elif current_stock <= reorder_point:
            return "Low Stock"
        return "In Stock"


