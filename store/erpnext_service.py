
from .erpnext_api import erpnext_api
from django.conf import settings
from decimal import Decimal

class ERPNextService:
    """
    Service layer to handle ERPNext integration logic
    """
    
    @staticmethod
    def is_enabled():
        """Check if ERPNext integration is enabled"""
        return getattr(settings, 'ERPNEXT_ENABLED', False)
    
    # Product/Item services
    @staticmethod
    def get_products(category=None, featured=None, limit=20):
        """Get products from ERPNext with optional filters"""
        if not ERPNextService.is_enabled():
            return []
        
        filters = {}
        if category:
            # If category is a slug (contains hyphens), convert to proper name
            if '-' in category:
                category = category.replace('-', ' ').title()
            filters['item_group'] = category
        if featured:
            filters['is_featured'] = 1
        
        response = erpnext_api.get_items(filters=filters, limit=limit)
        if response and 'data' in response:
            return ERPNextService._transform_items(response['data'])
        return []
    
    @staticmethod
    def get_product(item_code_or_slug):
        """Get single product from ERPNext by item code or slug"""
        if not ERPNextService.is_enabled():
            return None
        
        # Try to get by item code first
        response = erpnext_api.get_item(item_code_or_slug)
        if response and 'data' in response:
            return ERPNextService._transform_item(response['data'])
        
        # If not found, try to search by name (slug is derived from name)
        # Convert slug back to potential name
        search_name = item_code_or_slug.replace('-', ' ').title()
        items_response = erpnext_api.get_items(filters={'item_name': search_name}, limit=1)
        if items_response and 'data' in items_response and len(items_response['data']) > 0:
            return ERPNextService._transform_item(items_response['data'][0])
        
        return None
    
    @staticmethod
    def _transform_item(item_data):
        """Transform ERPNext item to frontend format"""
        item_name = item_data.get('item_name') or item_data.get('name', 'Unknown')
        item_id = item_data.get('name', item_name)
        category_name = item_data.get('item_group', '')
        
        # Fetch actual selling price from Item Price doctype
        price = Decimal('0')
        if item_id:
            price_response = erpnext_api.get_item_price(item_id)
            if price_response and 'data' in price_response and len(price_response['data']) > 0:
                # Get the first price record's rate
                price = Decimal(str(price_response['data'][0].get('price_list_rate', 0)))
            else:
                # Fallback to standard_rate if no Item Price found
                price = Decimal(str(item_data.get('standard_rate', 0)))
        
        return {
            'id': item_id,
            'name': item_name,
            'slug': item_id.lower().replace(' ', '-') if item_id else 'unknown',
            'description': item_data.get('description', ''),
            'price': price,
            'stock': item_data.get('actual_qty', 0),
            'image': item_data.get('image', ''),
            'category': category_name.lower().replace(' ', '-') if category_name else '',
            'category_name': category_name,
            'is_featured': item_data.get('is_featured', 0) == 1,
        }
    
    @staticmethod
    def _transform_items(items):
        """Transform multiple ERPNext items"""
        return [ERPNextService._transform_item(item) for item in items]
    
    # Category services
    @staticmethod
    def get_categories():
        """Get categories from ERPNext"""
        if not ERPNextService.is_enabled():
            return []
        
        response = erpnext_api.get_item_groups()
        if response and 'data' in response:
            return [ERPNextService._transform_category(cat) for cat in response['data']]
        return []
    
    @staticmethod
    def _transform_category(category_data):
        """Transform ERPNext item group to category format"""
        cat_name = category_data.get('item_group_name') or category_data.get('name', 'Unknown')
        cat_id = category_data.get('name', cat_name)
        
        return {
            'id': cat_id,
            'name': cat_name,
            'slug': cat_id.lower().replace(' ', '-') if cat_id else 'unknown',
            'description': category_data.get('description', ''),
            'image': category_data.get('image', ''),
        }
    
    # Order services
    @staticmethod
    def create_order(user, cart_items, shipping_info):
        """Create sales order in ERPNext"""
        if not ERPNextService.is_enabled():
            return None
        
        # Prepare customer data
        customer_id = f"CUST-{user.id}"
        
        # Create or get customer
        customer_data = {
            'customer_name': f"{user.first_name} {user.last_name}",
            'customer_type': 'Individual',
            'customer_group': 'Individual',
            'territory': 'All Territories',
        }
        erpnext_api.create_customer(customer_data)
        
        # Prepare order items
        items = []
        for cart_item in cart_items:
            items.append({
                'item_code': cart_item.product.name,  # or use item_code from ERPNext
                'qty': cart_item.quantity,
                'rate': float(cart_item.product.price),
            })
        
        # Create sales order
        order_data = {
            'customer': customer_id,
            'delivery_date': None,  # Set appropriate delivery date
            'items': items,
            'shipping_address': shipping_info.get('address'),
            'contact_email': shipping_info.get('email'),
            'contact_mobile': shipping_info.get('phone'),
        }
        
        response = erpnext_api.create_sales_order(order_data)
        return response
    
    # Stock services
    @staticmethod
    def get_stock_level(item_code):
        """Get stock level for an item"""
        if not ERPNextService.is_enabled():
            return 0
        
        response = erpnext_api.get_item_stock(item_code)
        if response and 'data' in response and len(response['data']) > 0:
            return sum([bin_data.get('actual_qty', 0) for bin_data in response['data']])
        return 0

# Singleton instance
erpnext_service = ERPNextService()
