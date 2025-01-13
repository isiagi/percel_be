from rest_framework.viewsets import ModelViewSet
from category.models import Category
from category.serializers import CategorySerializer

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer   