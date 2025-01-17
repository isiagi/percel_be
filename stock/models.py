from django.db import models
from users.models import CustomUser as User
from product.models import Product
from django.core.exceptions import ValidationError

# Create your models here.
class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
        ('ADJUST', 'Stock Adjustment')
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_movements')
    movement_type = models.CharField(max_length=6, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField()  # Can be negative for stock out
    reference = models.CharField(max_length=100, blank=True)  # e.g., "Sale #123", "Purchase #456"
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def clean(self):
        if self.movement_type == 'OUT':
            # Calculate available stock before this movement
            current_stock = self.product.available_stock
            if current_stock < self.quantity:
                raise ValidationError(f"Insufficient stock. Available: {current_stock}")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class StockAdjustment(models.Model):
    ADJUSTMENT_TYPES = [
        ('COUNT', 'Inventory Count'),
        ('DAMAGE', 'Damaged Goods'),
        ('LOSS', 'Lost Goods'),
        ('ADD', 'Add Stock'),
        ('REMOVE', 'Remove Stock'),
        ('OTHER', 'Other')
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='adjustments')
    adjustment_type = models.CharField(max_length=10, choices=ADJUSTMENT_TYPES)
    quantity = models.PositiveIntegerField()
    reason = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        current_stock = self.product.available_stock
        
        # Determine if this is addition or reduction based on adjustment type
        reduction_types = ['DAMAGE', 'LOSS', 'REMOVE']
        movement_type = 'OUT' if self.adjustment_type in reduction_types else 'IN'
        
        # For inventory counts, determine movement type based on difference
        if self.adjustment_type == 'COUNT':
            difference = self.quantity - current_stock
            movement_type = 'IN' if difference > 0 else 'OUT'
            self.quantity = abs(difference)  # Use absolute difference as quantity
        
        # Validate stock for reductions
        if movement_type == 'OUT' and current_stock < self.quantity:
            raise ValidationError(f"Insufficient stock. Available: {current_stock}")
            
        super().save(*args, **kwargs)
        
        # Create stock movement
        StockMovement.objects.create(
            product=self.product,
            movement_type=movement_type,
            quantity=self.quantity,
            reference=f'Adjustment #{self.id}',
            notes=f'{self.get_adjustment_type_display()}: {self.reason}',
            created_by=self.created_by
        )
