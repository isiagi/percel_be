from rest_framework import viewsets
from .models import Sale
from .serializers import SaleSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.db.models import Sum, F
from rest_framework.permissions import IsAuthenticated
from product.services import ProductStockService

# Create your views here.

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    # delete a sale, find product and add quantity back to stock using product stock service
    def perform_destroy(self, instance):
        for item in instance.items.all():
            product = item.product
            # product.available_stock += item.quantity
            # product.save()    
            ProductStockService.add_stock(product, item.quantity, f'Sale #{instance.id}', f'Return for sale deletion #{instance.id}', self.request.user)

        instance.delete()

    @action(detail=False, methods=['get'])
    def daily_sales(self, request):
        days = int(request.query_params.get('days', 7))
        start_date = datetime.now() - timedelta(days=days)
        
        sales = Sale.objects.filter(
            sale_date__gte=start_date
        ).values('sale_date__date').annotate(
            total_sales=Sum(F('items__quantity') * F('items__price'))
        ).order_by('sale_date__date')
        
        return Response(sales)
    
    # total amount of sales
    @action(detail=False, methods=['get'])
    def total_sales(self, request):
        total_sales = Sale.objects.aggregate(
            total=Sum(F('items__quantity') * F('items__price'))
        )['total'] or 0
        return Response({'total_sales': total_sales})
    
