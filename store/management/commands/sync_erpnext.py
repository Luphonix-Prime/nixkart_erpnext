
from django.core.management.base import BaseCommand
from store.erpnext_api import erpnext_api
from store.models import Product, Category
from django.utils.text import slugify

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
                
                product, created = Product.objects.update_or_create(
                    slug=slugify(product_name),
                    defaults={
                        'name': product_name,
                        'category': category,
                        'description': item_data.get('description', ''),
                        'price': item_data.get('standard_rate', 0),
                        'stock': item_data.get('actual_qty', 0),
                        'is_featured': item_data.get('is_featured', 0) == 1,
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created product: {product.name}'))
                else:
                    self.stdout.write(f'Updated product: {product.name}')
        
        self.stdout.write(self.style.SUCCESS('ERPNext sync completed!'))
