from rest_framework import serializers
from .models import Sale, SaleItem

class SaleItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    total_price = serializers.SerializerMethodField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)

    class Meta:
        model = SaleItem
        fields = ['id', 'product', 'notes', 'product_name', 'quantity', 'price', 'total_price']

    def get_total_price(self, obj):
        return obj.quantity * obj.price

class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True)
    total_amount = serializers.SerializerMethodField()
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Sale
        fields = ['id', 'customer', 'customer_name', 'sale_date', 'payment_method',
                 'notes', 'items', 'total_amount', 'created_by_name']
        read_only_fields = ['sale_date', 'created_by_name']

    
    def get_total_amount(self, obj):
        return obj.total_amount

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        sale = Sale.objects.create(**validated_data)
        
        for item_data in items_data:
            SaleItem.objects.create(sale=sale, notes=item_data.pop('notes', None), **item_data)
        
        return sale
        