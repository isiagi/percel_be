from rest_framework.viewsets import ModelViewSet
from product.models import Product
from product.serializers import ProductSerializer, ProductStockSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from stock.models import StockMovement, StockAdjustment
from stock.serializers import StockMovementSerializer
from .services import ProductStockService
from category.models import Category
from supplier.models import Supplier
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.exceptions import ValidationError
import cloudinary
import cloudinary.uploader


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductStockSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Product.objects.filter(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        product_data = request.data.copy()
        
        # Debug print statements
        print("Received Files:", request.FILES)
        print("Received Data:", product_data)
        
        # Validate category
        try:
            category = Category.objects.get(id=product_data.get('category'))
            product_data['category'] = category.id
        except Category.DoesNotExist:
            return Response({'error': 'Invalid category ID'}, status=400)
        
        # Validate supplier if provided
        supplier_id = product_data.get('supplier')
        if supplier_id:
            try:
                supplier = Supplier.objects.get(id=supplier_id)
                product_data['supplier'] = supplier.id
            except Supplier.DoesNotExist:
                return Response({'error': 'Invalid supplier ID'}, status=400)

        # Handle image upload to Cloudinary
        image_file = request.FILES.get('image')
        print("Image file:", image_file)  # Debug print
        
        if image_file:
            try:
                print("Attempting to upload to Cloudinary...")
                upload_result = cloudinary.uploader.upload(
                    image_file,
                    folder="products/",
                    resource_type="auto",
                    use_filename=True,
                    unique_filename=True
                )
                print("Cloudinary upload result:", upload_result)
                
                # Make sure image URL is properly set in product_data
                # Convert QueryDict to mutable dictionary if needed
                if hasattr(product_data, '_mutable'):
                    product_data._mutable = True
                product_data['image'] = upload_result['secure_url']
                print("Set image URL in product_data:", product_data['image'])  # Debug print
                
            except Exception as e:
                print(f"Cloudinary upload error: {str(e)}")
                return Response({
                    'error': f'Image upload failed: {str(e)}',
                    'detail': 'Error uploading to Cloudinary'
                }, status=400)
        
        try:
            initial_stock = int(product_data.get('initial_stock', 0))
            if 'initial_stock' in product_data:
                product_data.pop('initial_stock')
        except (ValueError, TypeError):
            return Response({'error': 'Invalid initial stock value'}, status=400)

        product_data['created_by'] = request.user.id

        try:
            print("Final product data:", product_data)
            serializer = self.get_serializer(data=product_data)
            print("Serializer initial data:", serializer.initial_data)  # Debug print
            
            if serializer.is_valid():
                print("Serializer validated data:", serializer.validated_data)  # Debug print
                product = serializer.save()
                print("Saved product image URL:", product.image)  # Debug print
                
                if initial_stock > 0:
                    ProductStockService.add_stock(
                        product=product,
                        quantity=initial_stock,
                        reference="Initial stock",
                        notes="Initial stock on product creation",
                        user=request.user
                    )
                
                # Get fresh serializer data
                result_serializer = self.get_serializer(product)
                return Response(result_serializer.data, status=status.HTTP_201_CREATED)
                
            print("Serializer errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            print(f"Error saving product: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        product_data = request.data.copy()

        # Handle image update
        image_file = request.FILES.get('image')
        if image_file:
            try:
                # Delete old image if it exists
                if instance.image and hasattr(instance.image, 'public_id'):
                    try:
                        cloudinary.uploader.destroy(instance.image.public_id)
                    except Exception as e:
                        print(f"Error deleting old image: {str(e)}")
                
                upload_result = cloudinary.uploader.upload(
                    image_file,
                    folder="products/",
                    resource_type="auto",
                    use_filename=True,
                    unique_filename=True
                )
                product_data['image'] = upload_result.get('secure_url')
            except Exception as e:
                return Response({
                    'error': f'Image upload failed: {str(e)}',
                    'detail': 'Error uploading to Cloudinary'
                }, status=400)

        # Handle category if present
        category_id = product_data.get('category')
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
                product_data['category'] = category.id
            except Category.DoesNotExist:
                return Response({'error': 'Invalid category ID'}, status=400)

        # Handle supplier if present
        supplier_id = product_data.get('supplier')
        if supplier_id:
            try:
                supplier = Supplier.objects.get(id=supplier_id)
                product_data['supplier'] = supplier.id
            except Supplier.DoesNotExist:
                return Response({'error': 'Invalid supplier ID'}, status=400)

        serializer = self.get_serializer(instance, data=product_data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_stock(self, request, pk=None):
        product = self.get_object()
        try:
            quantity = int(request.data.get('quantity', 0))
            reference = request.data.get('reference', '')
            notes = request.data.get('notes', '')
            ProductStockService.add_stock(product, quantity, reference, notes, request.user)
            return Response({'message': 'Stock added successfully'})
        except ValueError:
            return Response({'error': 'Invalid quantity value'}, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

    @action(detail=True, methods=['get'])
    def stock_history(self, request, pk=None):
        product = self.get_object()
        movements = StockMovement.objects.filter(product=product).order_by('-created_at')
        serializer = StockMovementSerializer(movements, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def adjust_stock(self, request, pk=None):
        product = self.get_object()
        try:
            adjustment_type = request.data.get('adjustment_type')
            quantity = int(request.data.get('quantity', 0))
            reason = request.data.get('reason', '')

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
            
        except ValueError:
            return Response({'error': 'Invalid quantity value'}, status=400)
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