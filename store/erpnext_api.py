
import requests
from django.conf import settings
import json
from decimal import Decimal

class ERPNextAPI:
    """
    API client for ERPNext integration
    """
    
    def __init__(self):
        # Get ERPNext configuration from environment or settings
        self.base_url = getattr(settings, 'ERPNEXT_URL', 'http://localhost:8000')
        self.api_key = getattr(settings, 'ERPNEXT_API_KEY', '')
        self.api_secret = getattr(settings, 'ERPNEXT_API_SECRET', '')
        
        self.headers = {
            'Authorization': f'token {self.api_key}:{self.api_secret}',
            'Content-Type': 'application/json'
        }
    
    def _make_request(self, method, endpoint, data=None):
        """Make HTTP request to ERPNext"""
        url = f"{self.base_url}/api/resource/{endpoint}"
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=self.headers, params=data)
            elif method == 'POST':
                response = requests.post(url, headers=self.headers, json=data)
            elif method == 'PUT':
                response = requests.put(url, headers=self.headers, json=data)
            elif method == 'DELETE':
                response = requests.delete(url, headers=self.headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"ERPNext API Error: {e}")
            return None
    
    # Product/Item methods
    def get_items(self, filters=None, fields=None, limit=20):
        """Get items from ERPNext"""
        params: dict[str, int | str] = {
            'limit_page_length': limit
        }
        if filters:
            params['filters'] = json.dumps(filters)
        if fields:
            params['fields'] = json.dumps(fields)
        
        return self._make_request('GET', 'Item', params)
    
    def get_item(self, item_code):
        """Get single item details"""
        return self._make_request('GET', f'Item/{item_code}')
    
    def get_item_groups(self):
        """Get item groups (categories)"""
        return self._make_request('GET', 'Item Group')
    
    def get_item_group(self, group_name):
        """Get single item group details"""
        return self._make_request('GET', f'Item Group/{group_name}')
    
    # Customer methods
    def create_customer(self, customer_data):
        """Create a new customer in ERPNext"""
        return self._make_request('POST', 'Customer', customer_data)
    
    def get_customer(self, customer_id):
        """Get customer details"""
        return self._make_request('GET', f'Customer/{customer_id}')
    
    def update_customer(self, customer_id, customer_data):
        """Update customer information"""
        return self._make_request('PUT', f'Customer/{customer_id}', customer_data)
    
    # Sales Order methods
    def create_sales_order(self, order_data):
        """Create a sales order in ERPNext"""
        return self._make_request('POST', 'Sales Order', order_data)
    
    def get_sales_order(self, order_id):
        """Get sales order details"""
        return self._make_request('GET', f'Sales Order/{order_id}')
    
    def get_sales_orders(self, customer=None):
        """Get all sales orders, optionally filtered by customer"""
        filters = {}
        if customer:
            filters['customer'] = customer
        return self._make_request('GET', 'Sales Order', {'filters': json.dumps(filters)})
    
    # Address methods
    def create_address(self, address_data):
        """Create an address in ERPNext"""
        return self._make_request('POST', 'Address', address_data)
    
    def get_addresses(self, customer=None):
        """Get addresses, optionally filtered by customer"""
        filters = {}
        if customer:
            filters['link_name'] = customer
        return self._make_request('GET', 'Address', {'filters': json.dumps(filters)})
    
    # Quotation methods
    def create_quotation(self, quotation_data):
        """Create a quotation (for cart)"""
        return self._make_request('POST', 'Quotation', quotation_data)
    
    def get_quotation(self, quotation_id):
        """Get quotation details"""
        return self._make_request('GET', f'Quotation/{quotation_id}')
    
    def update_quotation(self, quotation_id, quotation_data):
        """Update quotation"""
        return self._make_request('PUT', f'Quotation/{quotation_id}', quotation_data)
    
    # Stock methods
    def get_item_stock(self, item_code, warehouse=None):
        """Get item stock level"""
        filters = {'item_code': item_code}
        if warehouse:
            filters['warehouse'] = warehouse
        return self._make_request('GET', 'Bin', {'filters': json.dumps(filters)})
    
    # Price methods
    def get_item_price(self, item_code, price_list='Standard Selling'):
        """Get item price"""
        filters = {
            'item_code': item_code,
            'price_list': price_list,
            'selling': 1
        }
        fields = ['name', 'item_code', 'price_list', 'price_list_rate']
        params = {
            'filters': json.dumps(filters),
            'fields': json.dumps(fields)
        }
        return self._make_request('GET', 'Item Price', params)

    # ADD: Item create/update
    def create_item(self, item_data):
        """Create an Item"""
        return self._make_request('POST', 'Item', item_data)

    def update_item(self, item_code, item_data):
        """Update an Item"""
        return self._make_request('PUT', f'Item/{item_code}', item_data)

    # ADD: Item Group create (to ensure category exists)
    def create_item_group(self, group_data):
        """Create an Item Group"""
        return self._make_request('POST', 'Item Group', group_data)

    # ADD: Item Price create/update
    def create_item_price(self, price_data):
        """Create an Item Price"""
        return self._make_request('POST', 'Item Price', price_data)

    def update_item_price(self, price_name, price_data):
        """Update an Item Price"""
        return self._make_request('PUT', f'Item Price/{price_name}', price_data

# Singleton instance
erpnext_api = ERPNextAPI()
