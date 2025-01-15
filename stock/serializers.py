from rest_framework import serializers
from .models import StockMovement

class StockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = ['id', 'product', 'movement_type', 'quantity', 'reference', 'notes', 'created_at']