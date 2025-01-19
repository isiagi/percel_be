from rest_framework import serializers
from .models import Product
from category.models import Category

class ProductSerializer(serializers.ModelSerializer):
    stock_status = serializers.CharField(read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'description', 'price', 'initial_stock', 
                 'available_stock', 'reorder_point', 'stock_status', 'image', 
                 'created_at', 'updated_at', 'created_by']
        


class ProductStockSerializer(serializers.ModelSerializer):
    available_stock = serializers.IntegerField(read_only=True)
    initial_stock = serializers.IntegerField(read_only=True)
    stock_status = serializers.CharField(read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'price', 'initial_stock', 
                 'available_stock', 'stock_status', 'reorder_point','supplier', 'created_by', 'selling_price', 'cbm', 'description', 'image']