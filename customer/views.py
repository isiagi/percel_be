from rest_framework.viewsets import ModelViewSet
from customer.models import Customer
from customer.serializers import CustomerSerializer


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer   
