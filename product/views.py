from rest_framework.viewsets import ModelViewSet
from product.models import Product
from product.serializers import ProductSerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer    
