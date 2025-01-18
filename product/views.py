from rest_framework.viewsets import ModelViewSet
from product.models import Product
from product.serializers import ProductSerializer, ProductStockSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from stock.models import StockMovement
from stock.serializers import StockMovementSerializer
from stock.models import StockAdjustment
from .services import ProductStockService
from category.models import Category
from supplier.models import Supplier
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductStockSerializer
    permission_classes = [IsAuthenticated]

    token = Token.objects.get(key="ab71e9a8cd44705edb5e937e430f1bea2f22dee2")

    print(token.user)

    def get_queryset(self):
        return Product.objects.filter(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        product_data = request.data
        category_id = product_data.get('category')
        supplier_id = product_data.get('supplier')

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({'error': 'Invalid category ID'}, status=400)
        
        try:
            supplier = Supplier.objects.get(id=supplier_id)
        except Supplier.DoesNotExist:
            return Response({'error': 'Invalid supplier ID'}, status=400)

        initial_stock = int(product_data.pop('initial_stock', 0))
        user = request.user

        product_data['category'] = category  # Replace ID with the instance
        product_data['supplier'] = supplier  # Replace ID with the instance

        # Add the user as the created_by field
        product_data['created_by'] = user
        product = ProductStockService.create_product_with_stock(product_data, initial_stock, user)

        serializer = self.get_serializer(product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def add_stock(self, request, pk=None):
        product = self.get_object()
        quantity = int(request.data.get('quantity', 0))
        reference = request.data.get('reference', '')
        notes = request.data.get('notes', '')
        user = request.user
        ProductStockService.add_stock(product, quantity, reference, notes, user)
        return Response({'message': 'Stock added successfully'})

    @action(detail=True, methods=['get'])
    def stock_history(self, request, pk=None):
        product = self.get_object()
        print(product)
        movements = StockMovement.objects.filter(product=product).order_by('-created_at')
        serializer = StockMovementSerializer(movements, many=True)
        return Response(serializer.data)
    

    @action(detail=True, methods=['post'])
    def adjust_stock(self, request, pk=None):
        product = self.get_object()
        adjustment_type = request.data.get('adjustment_type')
        quantity = int(request.data.get('quantity', 0))
        reason = request.data.get('reason', '')

        try:
            adjustment = StockAdjustment.objects.create(
                product=product,
                adjustment_type=adjustment_type,
                quantity=quantity,
                reason=reason,
                created_by=request.user
            )
            
            return Response({
                'message': 'Stock adjusted successfully',
                'adjustment_type': adjustment.get_adjustment_type_display(),
                'quantity': quantity,
                'current_stock': product.available_stock
            })
            
        except ValidationError as e:
            return Response({'error': str(e)}, status=400)
        except Exception as e:
            return Response({'error': 'Failed to adjust stock'}, status=400)

    @action(detail=True, methods=['get'])
    def adjustment_history(self, request, pk=None):
        product = self.get_object()
        adjustments = product.adjustments.all().order_by('-date')
        serializer = StockAdjustmentSerializer(adjustments, many=True)
        return Response(serializer.data)
