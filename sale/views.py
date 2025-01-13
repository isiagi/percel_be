from rest_framework import viewsets
from .models import Sale
from .serializers import SaleSerializer

# Create your views here.

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    
