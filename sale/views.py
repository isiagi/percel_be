from rest_framework import viewsets
from .models import Sale
from .serializers import SaleSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.db.models import Sum, F

# Create your views here.

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

    # def perform_create(self, serializer):
    #     serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def daily_sales(self, request):
        days = int(request.query_params.get('days', 7))
        start_date = datetime.now() - timedelta(days=days)
        
        sales = Sale.objects.filter(
            sale_date__gte=start_date
        ).values('sale_date__date').annotate(
            total_sales=Sum(F('items__quantity') * F('items__unit_price'))
        ).order_by('sale_date__date')
        
        return Response(sales)
    
