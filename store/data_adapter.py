
from django.conf import settings
from .models import Product, Category, Order
from .erpnext_service import erpnext_service

class DataAdapter:
    """
    Adapter to switch between Django models and ERPNext data
    """
    
    @staticmethod
    def use_erpnext():
        """Check if ERPNext should be used"""
        return getattr(settings, 'ERPNEXT_ENABLED', False)
    
    @staticmethod
    def get_products(category=None, featured=None, limit=None):
        """Get products from either Django or ERPNext"""
        if DataAdapter.use_erpnext():
            return erpnext_service.get_products(category=category, featured=featured, limit=limit or 20)
        else:
            queryset = Product.objects.all()
            if category:
                queryset = queryset.filter(category__slug=category)
            if featured:
                queryset = queryset.filter(is_featured=True)
            if limit:
                queryset = queryset[:limit]
            return queryset
    
    @staticmethod
    def get_product(product_id):
        """Get single product"""
        if DataAdapter.use_erpnext():
            return erpnext_service.get_product(product_id)
        else:
            try:
                return Product.objects.get(slug=product_id)
            except Product.DoesNotExist:
                return None
    
    @staticmethod
    def get_categories():
        """Get categories"""
        if DataAdapter.use_erpnext():
            return erpnext_service.get_categories()
        else:
            return Category.objects.all()
    
    @staticmethod
    def create_order(user, cart_items, shipping_info):
        """Create order in ERPNext or Django"""
        if DataAdapter.use_erpnext():
            return erpnext_service.create_order(user, cart_items, shipping_info)
        else:
            # Create Django order
            from .models import Order, OrderItem
            order = Order.objects.create(
                user=user,
                full_name=shipping_info.get('full_name', ''),
                email=shipping_info.get('email', ''),
                phone=shipping_info.get('phone', ''),
                address=shipping_info.get('address', ''),
                city=shipping_info.get('city', ''),
                state=shipping_info.get('state', ''),
                zip_code=shipping_info.get('zip_code', ''),
                country=shipping_info.get('country', ''),
                total=sum(item.subtotal() for item in cart_items)
            )
            
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product_name=item.product.name,
                    product_price=item.product.price,
                    quantity=item.quantity,
                    subtotal=item.subtotal()
                )
            
            return order
