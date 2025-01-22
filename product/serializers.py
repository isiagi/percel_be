from rest_framework import serializers
from .models import Product
from category.models import Category

class ProductSerializer(serializers.ModelSerializer):
    stock_status = serializers.CharField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'description', 'price', 'initial_stock', 
                 'available_stock', 'reorder_point', 'stock_status', 'image', 'quantity',
                 'created_at', 'updated_at', 'created_by']
        


class ProductStockSerializer(serializers.ModelSerializer):
    available_stock = serializers.IntegerField(read_only=True)
    initial_stock = serializers.IntegerField(read_only=True)
    stock_status = serializers.CharField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    category_name = serializers.CharField(source='category.name', read_only=True)
    total_investment = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    realized_returns = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    potential_returns = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_returns = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'price', 'initial_stock', 
                 'available_stock', 'stock_status', 'reorder_point','supplier', 'created_by', 'selling_price', 'cbm', 'description', 'image', 'category_name', 'created_at', 'updated_at'
                 , 'total_investment', 'realized_returns', 'potential_returns', 'total_returns']