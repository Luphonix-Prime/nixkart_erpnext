
from django.core.management.base import BaseCommand
from store.erpnext_api import erpnext_api
from store.models import Product, Category
from django.utils.text import slugify
from decimal import Decimal

class Command(BaseCommand):
    help = 'Sync products and categories from ERPNext'

    def handle(self, *args, **options):
        self.stdout.write('Starting ERPNext sync...')
        
        # Sync categories
        self.stdout.write('Syncing categories...')
        categories_response = erpnext_api.get_item_groups()
        if categories_response and 'data' in categories_response:
            for cat_data in categories_response['data']:
                # ERPNext uses 'name' for both the ID and display name
                category_name = cat_data.get('item_group_name') or cat_data.get('name')
                if not category_name:
                    self.stdout.write(self.style.WARNING(f'Skipping category with no name: {cat_data}'))
                    continue
                    
                category, created = Category.objects.update_or_create(
                    slug=slugify(category_name),
                    defaults={
                        'name': category_name,
                        'description': cat_data.get('description', ''),
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))
                else:
                    self.stdout.write(f'Updated category: {category.name}')
        else:
            self.stdout.write(self.style.WARNING('Could not fetch categories from ERPNext. Using local data.'))
        
        # Sync products
        self.stdout.write('Syncing products...')
        items_response = erpnext_api.get_items(limit=100)
        if items_response and 'data' in items_response:
            for item_data in items_response['data']:
                # Get product name
                product_name = item_data.get('item_name') or item_data.get('name')
                if not product_name:
                    self.stdout.write(self.style.WARNING(f'Skipping product with no name: {item_data}'))
                    continue
                
                # Get or create category
                category_name = item_data.get('item_group', 'Uncategorized')
                category, _ = Category.objects.get_or_create(
                    slug=slugify(category_name),
                    defaults={'name': category_name}
                )
                
                # Fetch actual selling price from Item Price doctype
                price = Decimal('0')
                item_code = item_data.get('name')  # ERPNext item code
                if item_code:
                    price_response = erpnext_api.get_item_price(item_code)
                    if price_response and 'data' in price_response and len(price_response['data']) > 0:
                        price = Decimal(str(price_response['data'][0].get('price_list_rate', 0)))
                    else:
                        price = Decimal(str(item_data.get('standard_rate', 0)))
                
                # Get stock level from Bin doctype
                stock = 0
                if item_code:
                    stock_response = erpnext_api.get_item_stock(item_code)
                    if stock_response and 'data' in stock_response and len(stock_response['data']) > 0:
                        # Prefer projected_qty if present; fallback to actual_qty
                        total = 0
                        for bin_data in stock_response['data']:
                            qty = bin_data.get('projected_qty')
                            if qty is None:
                                qty = bin_data.get('actual_qty', 0)
                            total += max(qty or 0, 0)
                        stock = total
                
                # Get the ERPNext item code
                item_code = item_data.get('name')  # ERPNext item code
                
                product, created = Product.objects.update_or_create(
                    slug=slugify(product_name),  # Use slug as the unique identifier
                    defaults={
                        'name': product_name,
                        'category': category,
                        'description': item_data.get('description', ''),
                        'price': price,
                        'stock': stock,
                        'is_featured': item_data.get('is_featured', 0) == 1,
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created product: {product.name}'))
                else:
                    self.stdout.write(f'Updated product: {product.name}')
        else:
            self.stdout.write(self.style.WARNING('Could not fetch products from ERPNext. Using local data.'))
        
        self.stdout.write(self.style.SUCCESS('ERPNext sync completed!'))
