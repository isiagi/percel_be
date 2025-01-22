from rest_framework import serializers
from .models import StockMovement

class StockMovementSerializer(serializers.ModelSerializer):
    product_image = serializers.ImageField(source='product.image', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_available_stock = serializers.IntegerField(source='product.available_stock', read_only=True)
    class Meta:
        model = StockMovement
        fields = ['id', 'product', 'movement_type', 'quantity', 'product_image', 'reference', 'product_price', 'product_available_stock', 'product_name', 'notes', 'created_at']