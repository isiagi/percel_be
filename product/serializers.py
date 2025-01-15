from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    stock_status = serializers.CharField(read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'description', 'price', 'initial_stock', 
                 'available_stock', 'reorder_point', 'stock_status', 'image', 
                 'created_at', 'updated_at']