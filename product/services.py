from product.models import Product
from stock.models import StockMovement


class ProductStockService:
    @staticmethod
    def create_product_with_stock(product_data, initial_stock, user):
        """Create a product with initial stock"""
        product = Product.objects.create(**product_data)
        
        # Create initial stock movement
        StockMovement.objects.create(
            product=product,
            movement_type='IN',
            quantity=initial_stock,
            reference='Initial Stock',
            notes='Initial stock on product creation',
            created_by=user
        )
        
        return product

    @staticmethod
    def add_stock(product, quantity, reference, notes, user):
        """Add stock to product"""
        return StockMovement.objects.create(
            product=product,
            movement_type='IN',
            quantity=quantity,
            reference=reference,
            notes=notes,
            created_by=user
        )

    @staticmethod
    def remove_stock(product, quantity, reference, notes, user):
        """Remove stock from product"""
        return StockMovement.objects.create(
            product=product,
            movement_type='OUT',
            quantity=quantity,
            reference=reference,
            notes=notes,
            created_by=user
        )